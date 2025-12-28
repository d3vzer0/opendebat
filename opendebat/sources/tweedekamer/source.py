import dlt
from dlt.sources.helpers.rest_client.client import RESTClient
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
from dlt.sources.helpers.rest_client.paginators import (
    SinglePagePaginator,
)
from opendebat.sources.tweedekamer.models.verslag import Vergadering
from opendebat.sources.tweedekamer.models.segment import flatten_speakers
import xmltodict


@dlt.source(max_table_nesting=0)
def tweedekamer():

    debatclient = RESTClient(
        base_url="https://gegevensmagazijn.tweedekamer.nl",
        paginator=SinglePagePaginator(),
    )

    @dlt.resource(parallelized=True)
    def vergaderingen():
        # filter = "year(Datum) eq 2025"
        filter = "year(Datum) eq 2025 and month(Datum) eq 3"

        response = debatclient.get(
            "/OData/v4/2.0/Vergadering", params={"$filter": filter, "$count": "true"}
        ).json()
        for vergadering in response["value"]:
            yield vergadering

    @dlt.transformer(data_from=vergaderingen, parallelized=True)
    def verslag(vergadering):
        filter = f"Vergadering_Id eq {vergadering['Id']}"
        response = debatclient.get(
            "/OData/v4/2.0/Verslag", params={"$filter": filter}
        ).json()
        for verslag in response["value"]:
            yield {"vergadering": vergadering["Id"], **verslag}

    @dlt.transformer(data_from=verslag, parallelized=True)
    def verslag_content(verslag):
        response = debatclient.get(
            f"/OData/v4/2.0/verslag/{verslag['Id']}/resource"
        ).content
        response = xmltodict.parse(response)
        document_content = response["vlosCoreDocument"]
        vergadering = document_content["vergadering"]
        yield vergadering

    @dlt.transformer(data_from=verslag_content, parallelized=True)
    def segments(verslag):

        vergadering = Vergadering(**verslag)
        for activiteit in vergadering.activiteit:
            hoofden = activiteit.activiteithoofd
            if not isinstance(hoofden, list):
                hoofden = [hoofden]

            for hoofd in hoofden:
                if hoofd.activiteitdeel is None:
                    continue

                delen = hoofd.activiteitdeel
                if not isinstance(delen, list):
                    delen = [delen]

                for deel in delen:
                    yield flatten_speakers(
                        deel.activiteititem.woordvoerder,
                        vergadering.titel,
                        vergadering.datum,
                        vergadering.aanvangstijd,
                        vergadering.sluiting,
                        activiteit.titel,
                    )

    return segments
