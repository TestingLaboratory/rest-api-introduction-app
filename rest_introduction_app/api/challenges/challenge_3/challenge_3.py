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

# TODO basic auth
# TODO Flags
# TODO Make a copy of isolated RNA
# TODO index length, letters validation

from fastapi import APIRouter, Query
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(prefix="/challenge/3")

sequence = {
    "isolated": "GUCAUUCUCCUAAGAAGCUAUUAGGCUAGGCCUAAUGCCCGAUCGA",
    "copy": "GUCAUUCUCCUAAGAAGCUAUUAGGCUAGGCCUAAUGCCCGAUCGA"
}

achievement_counter = {"nucleocreator": 0,
                       "aminoacid_appender": 0,
                       "mutator": 0,
                       "reductor": 0,
                       "erdaicator": 0,
                       "architect": 0,
                       "observer": 0
                       }

flags = dict(nucleocreator=False, aminoacid_appender=False, mutator=False, reductor=False, erdaicator=False,
             architect=False, observer=False)


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"You are the Genome Researcher. "
                   f"You are meddling with Coronavirus SARS-Cov-2 RNA... "
                   f"Try to change the RNA at your disposal to uncover as many medical breakthroughs as possible. "
                   f"use GET /sample to see the original RNA strand "
                   f"use COPY /sample to create exact duplicate of original to perform experiments. "
                   f"Try to change the RNA at your disposal to uncover as many medical breakthroughs as possible. "
                   f"Good luck researcher. "
                   f"Our souls fates' depend on you! "
    }


@router.get("/check_flags", status_code=status.HTTP_200_OK)
async def achievements():
    """
    Get this resource to obtain your research progress
    """
    return {
        "achievements": flags
    }


@router.get("/sample", status_code=status.HTTP_200_OK)
async def get_rna():
    """
    Get this resource to obtain your research material
    """
    return {
        "sample": sequence["copy"].replace("_", "")
    }


# Tutaj pewnie chodziło o wyświtlenie x tripletów od początku sekwencji? Można zmienić :)
@router.get("/triplets/{number}", status_code=status.HTTP_200_OK)
async def get_triplet(number: int):
    triplet_index = (number - 1) * 3
    if triplet_index < len(sequence["copy"]) - 3:
        return {
            f"triplet at position {number}": "".join(sequence["copy"][triplet_index: triplet_index + 3])
        }
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Check the length of your sequence. It's not as long as you think."
            }
        )


@router.post("/triplets/", status_code=status.HTTP_201_CREATED)
async def add_triplet(triplet_to_add: str = Query(..., min_length=3, max_length=3)):
    sequence["copy"] = sequence["copy"] + triplet_to_add
    return {
        "message": "Bravo! You've elongated the RNA strand you molecular freak! To check it's sequence use GET /sample"
    }


@router.put("/triplets/{triplet_id}", status_code=status.HTTP_200_OK)
async def triplet_replacement(triplet_id: int,
                              triplet_to_add: str = Query(..., min_length=3, max_length=3)):
    sequence_list = list(sequence["copy"])
    index = (triplet_id - 1) * 3
    sequence_list[index:index + 3] = list(triplet_to_add)
    sequence["copy"] = "".join(sequence_list)
    return {
        "message": "Substitution of a triplet went smoothly. "
                   "To check the sequence use GET /sample"
    }


@router.delete("/triplets/{triplet_id}", status_code=status.HTTP_202_ACCEPTED)
async def triplet_deletion(triplet_id: int):
    sequence_list = list(sequence["copy"])
    index = (triplet_id - 1) * 3
    sequence_list[index:index + 3] = ("_", "_", "_")
    sequence["copy"] = "".join(sequence_list)
    return {
        "message": "You are a master of restriction enzymes, you've cut out a part of RNA. "
                   "To check the sequence after the process use GET /sample"
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def get_nucleotide(number: int):
    sequence["copy"] = sequence["copy"].replace("_", "")
    if number < len(sequence["copy"]):
        return sequence["copy"][number - 1]
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Check the length of your sequence. It's not as long as you think."
            }
        )


@router.post("/nucleotides/", status_code=status.HTTP_201_CREATED)
async def add_triplet(nucleotide_to_add: str = Query(..., min_length=1, max_length=1)):
    sequence["copy"] = sequence["copy"] + nucleotide_to_add
    return {
        "message": "That's one small nucleotide for man, but could be a one giant leap for mankind, keep going lab rat! "
                   "To check the sequence use GET /sample"
    }


@router.put("/nucleotides/{nucleotide_id}", status_code=status.HTTP_200_OK)
async def nucleotide_replacement(nucleotide_id: int,
                                 nucleotide_to_add: str = Query(..., min_length=1, max_length=1)):
    sequence_list = list(sequence["copy"])
    sequence_list[nucleotide_id - 1:nucleotide_id] = nucleotide_to_add
    sequence["copy"] = "".join(sequence_list)
    return {
        "message": "Substitution of a nucleotide went smoothly. Change your gloves and keep going!"
                   "To check the sequence use GET /sample"
    }


@router.delete("/nucleotides/{nucleotide_id}", status_code=status.HTTP_202_ACCEPTED)
async def nucleotide_deletion(nucleotide_id: int):
    sequence_list = list(sequence["copy"])
    sequence_list[nucleotide_id - 1:nucleotide_id] = "_"
    sequence["copy"] = "".join(sequence_list)
    return {
        "message": "You are a master of restriction enzymes, you've cut out a part of RNA. "
                   "To check the sequence after the process use GET /sample"
    }


# def translate(seq):
#     table = {"UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
#              "UCU": "S", "UCC": "s", "UCA": "S", "UCG": "S",
#              "UAU": "Y", "UAC": "Y", "UAA": "STOP", "UAG": "STOP",
#              "UGU": "C", "UGC": "C", "UGA": "STOP", "UGG": "W",
#              "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
#              "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
#              "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
#              "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
#              "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
#              "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
#              "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
#              "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
#              "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
#              "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
#              "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
#              "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
#              }
#     protein = ""
#     if len(seq) % 3 == 0:
#         for i in range(0, len(seq), 3):
#             codon = seq[i:i + 3]
#             amino = table[codon]
#             protein += amino
#     return protein
