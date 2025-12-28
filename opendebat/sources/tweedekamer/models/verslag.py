from pydantic import BaseModel, Field, computed_field, PrivateAttr
from datetime import datetime


# TODO: Dit moet vast beter kunnen maar yolo
def parse_alinea(tekst):
    plaintext = ""
    if "alinea" in tekst:
        if isinstance(tekst["alinea"], list):
            for item in tekst["alinea"]:
                if isinstance(item["alineaitem"], list):
                    plaintext += item["alineaitem"][1]
                elif isinstance(item["alineaitem"], str):
                    plaintext += item["alineaitem"]

        if isinstance(tekst["alinea"], dict):
            if isinstance(tekst["alinea"]["alineaitem"], list):
                plaintext += tekst["alinea"]["alineaitem"][1]
    return plaintext


class Spreker(BaseModel):
    voornaam: str
    achternaam: str


class Interumpant(BaseModel):
    tekst: dict = Field(exclude=True)
    interrumpant: "Interumpant | list[Interumpant] | None" = None

    @computed_field
    def tekst_plain(self) -> str:
        result = parse_alinea(self.tekst)
        return result


class Woordvoerder(BaseModel):
    spreker: Spreker
    tekst: dict = Field(exclude=True)
    interrumpant: "Interumpant | list[Interumpant] | None" = None

    @computed_field
    def tekst_plain(self) -> str:
        result = parse_alinea(self.tekst)
        return result


class Activiteititem(BaseModel):
    soort: str = Field(alias="@soort")
    titel: str
    markeertijdbegin: datetime
    markeertijdeind: datetime
    woordvoerder: Woordvoerder | list[Woordvoerder] | None = None


class Activiteitdeel(BaseModel):
    # spreker:
    titel: str
    activiteititem: Activiteititem


class Activiteithoofd(BaseModel):
    soort: str = Field(alias="@soort")
    titel: str
    markeertijdbegin: datetime
    markeertijdeind: datetime
    activiteitdeel: Activiteitdeel | list[Activiteitdeel] | None = None
    # draadboekfragment: Draadboekfragment


class Activiteit(BaseModel):
    soort: str = Field(alias="@soort")
    titel: str
    onderwerp: str
    aanvangstijd: datetime
    eindtijd: datetime
    parlisid: str | None = None
    activiteithoofd: Activiteithoofd | list[Activiteithoofd]


class Vergadering(BaseModel):
    soort: str = Field(alias="@soort")
    kamer: str = Field(alias="@kamer")
    titel: str
    zaal: str
    vergaderjaar: str
    vergaderingnummer: int
    datum: datetime
    aanvangstijd: datetime
    sluiting: datetime
    activiteit: list[Activiteit]
