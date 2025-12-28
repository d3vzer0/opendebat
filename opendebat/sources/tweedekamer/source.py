import dlt
from dlt.sources.helpers.rest_client.client import RESTClient
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
from dlt.sources.helpers.rest_client.paginators import (
    SinglePagePaginator,
)
from opendebat.sources.tweedekamer.models.verslag import Vergadering
import xmltodict


@dlt.source(max_table_nesting=0)
def tweedekamer():

    debatclient = RESTClient(
        base_url="https://gegevensmagazijn.tweedekamer.nl",
        paginator=SinglePagePaginator(),
    )

    @dlt.resource(parallelized=True)
    def vergaderingen():
        filter = "year(Datum) eq 2025"
        response = debatclient.get(
            "/OData/v4/2.0/Vergadering", params={"$filter": filter, "$count": "true"}
        ).json()
        for vergadering in response["value"][0:1]:
            yield vergadering

    @dlt.transformer(data_from=vergaderingen)
    def verslag(vergadering):
        filter = f"Vergadering_Id eq {vergadering['Id']}"
        response = debatclient.get(
            "/OData/v4/2.0/Verslag", params={"$filter": filter}
        ).json()
        for verslag in response["value"]:
            yield {"vergadering": vergadering["Id"], **verslag}

    @dlt.transformer(data_from=verslag, columns=Vergadering)
    def verslag_content(verslag):
        response = debatclient.get(
            f"/OData/v4/2.0/verslag/{verslag['Id']}/resource"
        ).content
        response = xmltodict.parse(response)
        document_content = response["vlosCoreDocument"]
        vergadering = document_content["vergadering"]
        yield vergadering

    return (vergaderingen, verslag, verslag_content)
