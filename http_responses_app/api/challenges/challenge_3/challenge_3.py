# TODO challenge
# TODO Paweł Muzyka - genetyka
## challenge 3
## genom z tripletami
# tym razem basic auth
# endpointy
# GET /rna filtruje wszystkie ustawione na none lub "" i buduje białko na podstawie łańcucha nukleotydów
# GET/PUT/PATCH/POST/DELETE triplets/{number}
# GET/PUT/PATCH/POST/DELETE nucleotides/{number}
# flagi - nucleocreator - po 10 postach nowych nukleotydów
# flagi - aminoacid_appender - po 10 postach nowych tripletów
# flaga - mutator - po 10 patchach w tripletach
# flaga - reduktor - po 10 deletach w tripletach
# flaga eradicator - po usunięciu całego kodu RNA
# flaga architect po dodaniu 50 postów tripletów i zdobyciu flagi architekt
# flaga observer po 5 getach na /rna

from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(prefix="/challenge/3")


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"You are the Genome Researcher. "
                   f"You are meddling with Coronavirus Sars-Cov-2 RNA... "
                   f"Try to change the RNA at your disposal to uncover as many medical breakthroughs as possible. "
                   f"use GET /sample to see the original RNA strand "
                   f"use COPY /sample to create exact duplicate of original to perform experiments. "
                   f"Try to change the RNA at your disposal to uncover as many medical breakthroughs as possible. "
                   f"Good luck researcher. "
                   f"Our souls fates' depend on you! "
    }
