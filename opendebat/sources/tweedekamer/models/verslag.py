from pydantic import BaseModel, Field, computed_field, PrivateAttr
from datetime import datetime


from dataclasses import dataclass
from datetime import datetime


# TODO: Dit moet vast beter kunnen maar yolo
def parse_alinea(tekst):
    plaintext = ""
    if "alinea" in tekst:
        if isinstance(tekst["alinea"], list):
            for item in tekst["alinea"]:
                if "alineaitem" in item:
                    if isinstance(item["alineaitem"], list):
                        if isinstance(item["alineaitem"][1], str):
                            plaintext += item["alineaitem"][1]
                        # TODO: Handle this!
                        # else:
                        #     print(item["alineaitem"])
                    elif isinstance(item["alineaitem"], str):
                        plaintext += item["alineaitem"]

                if "lijst" in item:
                    if "alineaitem" in item["lijst"]:
                        if isinstance(item["lijst"]["alineaitem"], list):
                            for lijstitem in item["lijst"]["alineaitem"]:
                                if isinstance(item["lijst"]["alineaitem"], str):
                                    plaintext += lijstitem
                                # TODO: HANDLE THIS
                        if isinstance(item["lijst"]["alineaitem"], str):
                            plaintext += item["lijst"]["alineaitem"]

                #     plaintext += item["lijst"]["alineaitem"]
                # else:
                #     print(item)

        if isinstance(tekst["alinea"], dict):
            if isinstance(tekst["alinea"]["alineaitem"], list):
                if isinstance(tekst["alinea"]["alineaitem"][1], str):
                    plaintext += tekst["alinea"]["alineaitem"][1]

                # TODO: HANDLE THIS
                # if isinstance(tekst["alinea"]["alineaitem"][1], dict):
                #     if "nadruk" in tekst["alinea"]["alineaitem"][1]:

                # else:
                #     print(tekst["alinea"]["alineaitem"][1])
    return plaintext


class Spreker(BaseModel):
    voornaam: str
    achternaam: str

    @computed_field
    def naam(self) -> str:
        return f"{self.voornaam} {self.achternaam}"


class Interumpant(BaseModel):
    tekst: dict | None = Field(exclude=True, default=None)
    interrumpant: "Interumpant | list[Interumpant] | None" = None
    spreker: Spreker | None = None
    markeertijdbegin: datetime
    markeertijdeind: datetime

    @computed_field
    def tekst_plain(self) -> str:
        result = ""
        if self.tekst:
            result = parse_alinea(self.tekst)
        return result


class Woordvoerder(BaseModel):
    spreker: Spreker
    tekst: dict | None = Field(exclude=True, default=None)
    interrumpant: "Interumpant | list[Interumpant] | None" = None
    markeertijdbegin: datetime
    markeertijdeind: datetime

    @computed_field
    def tekst_plain(self) -> str:
        result = ""
        if self.tekst:
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
    activiteititem: Activiteititem | None = None


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
