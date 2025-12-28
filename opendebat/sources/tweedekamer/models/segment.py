from pydantic import BaseModel
from .verslag import Vergadering, Interumpant, Woordvoerder
from datetime import datetime


class SpokenSegment(BaseModel):
    vergadering_titel: str
    vergadering_datum: datetime
    vergadering_start: datetime
    vergadering_eind: datetime
    activiteit_titel: str
    spreker_voornaam: str
    spreker_achternaam: str
    tekst: str
    tijdstip_start: datetime
    tijdstip_eind: datetime


def flatten_speakers(
    node: Woordvoerder | Interumpant | list[Woordvoerder] | list[Interumpant] | None,
    vergadering_titel: str,
    vergadering_datum: datetime,
    vergadering_start: datetime,
    vergadering_eind: datetime,
    activiteit_titel: str,
) -> list[SpokenSegment]:
    if node is None:
        return []

    results = []
    items = node if isinstance(node, list) else [node]

    for item in items:
        if item.tekst_plain and item.spreker:
            results.append(
                SpokenSegment(
                    vergadering_titel=vergadering_titel,
                    vergadering_datum=vergadering_datum,
                    vergadering_start=vergadering_start,
                    vergadering_eind=vergadering_eind,
                    activiteit_titel=activiteit_titel,
                    spreker_voornaam=item.spreker.voornaam,
                    spreker_achternaam=item.spreker.achternaam,
                    tekst=item.tekst_plain,
                    tijdstip_start=item.markeertijdbegin,
                    tijdstip_eind=item.markeertijdeind,
                )
            )

        if item.interrumpant:
            results.extend(
                flatten_speakers(
                    item.interrumpant,
                    vergadering_titel,
                    vergadering_datum,
                    vergadering_start,
                    vergadering_eind,
                    activiteit_titel,
                )
            )

    return results
