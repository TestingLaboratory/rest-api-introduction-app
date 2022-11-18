from typing import List

from fastapi import APIRouter, Query, HTTPException, Depends, Path
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_3.model import TechnicianCheckIn, LabTechnician

challenge_tag = "Challenge - Virology: the Genetic Research."
challenge_prefix = "/challenge/genetics"
router = APIRouter(prefix=challenge_prefix)
security = HTTPBasic()

#TODO use real RNA for Sars-Cov-2
#TODO perform mutations and prepare translation algorithm for the sequence
#TODO Prepare "viruspedia" to include inforamtion about DNA/RNA translation, list of amino acid, etc.

sequence = {
    "isolated": "GUCAUUCUCCUAAGAAGCUAUUAGGCUAGGCCUAAUGCCCGAUCGA",
    "copy": "GUCAUUCUCCUAAGAAGCUAUUAGGCUAGGCCUAAUGCCCGAUCGA"
}

TECHNICIANS: List[LabTechnician] = []


def message_for_researcher(credentials: HTTPBasicCredentials):
    if is_winner(credentials):
        message = "CONGRATS! YOUR RNA IS READY TO TRANSLATE INTO PROTEIN! \n USE /translate ENDPOINT"
    else:
        message = "Maybe watch Andromeda Strain movie for some reference..."
    return message


def is_winner(credentials: HTTPBasicCredentials):
    lab_technician = next(filter(lambda technician: technician.name == credentials.username, TECHNICIANS), None)
    lab_technician.calculate_achievements()
    return all(lab_technician.achievements[achievement] for achievement in lab_technician.achievements)


def has_credentials(credentials: HTTPBasicCredentials):
    technician = LabTechnician(credentials.username, credentials.password)
    if technician not in TECHNICIANS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"}
        )
    else:
        return True


def verify_triplet_id(triplet_id: int):
    if not triplet_id <= int(len(sequence["copy"].replace("_", "")) / 3) or triplet_id <= 0:
        raise HTTPException(status_code=422, detail="triplet_id is beyond the length of RNA")


def verify_nucleotide_id(nucleotide_id: int):
    if not nucleotide_id <= int(len(sequence["copy"].replace("_", ""))) or nucleotide_id <= 0:
        raise HTTPException(status_code=422, detail="nucleotide_id is beyond the length of RNA")


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"You are the Genome Researcher. "
                   f"You are meddling with Coronavirus SARS-Cov-2 RNA... "
                   f"Try to change the RNA at your disposal to uncover as many medical breakthroughs as possible. "
                   f"use GET /primary_sequence to see the original RNA strand "
                   f"use GET /sample_sequence to create exact duplicate of original to perform experiments. "
                   f"Try to change the RNA at your disposal to uncover as many medical breakthroughs as possible. "
                   f"Good luck researcher. "
                   f"Our souls fates' depend on you! "
    }


@router.post("/register_as_technician")
async def register(credentials: TechnicianCheckIn):
    lab_technician = LabTechnician(credentials.username, credentials.password)
    content = {"message": None}
    if lab_technician in TECHNICIANS:
        status_code = status.HTTP_400_BAD_REQUEST
        content["message"] = "You are already a member of COVID research team."
    else:
        TECHNICIANS.append(lab_technician)
        status_code = status.HTTP_201_CREATED
        content["message"] = f"You have been registered {lab_technician.name}."
        f"Take your hazmat suit, and do not forget about procedures!"

    return JSONResponse(
        content=content,
        status_code=status_code
    )


@router.get("/check_flags", status_code=status.HTTP_200_OK)
async def achievements(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get this resource to obtain your research progress
    """
    if has_credentials(credentials):
        lab_technician = next(filter(lambda technician: technician.name == credentials.username, TECHNICIANS), None)
        return {
            "achievements": lab_technician.achievements,
            "proteomaster_flag": lab_technician.proteomaster
        }


@router.get("/primary_sequence", status_code=status.HTTP_200_OK)
async def get_sequence(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get this resource to obtain sequence of the matrix
    """
    if has_credentials(credentials):
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "primary_sequence": sequence["isolated"],
            "message": "This is a sequence of isolated, unmodified RNA sample."
                       f" You can compare your copy with this sequence. {additional_message_for_researcher}"
        }


@router.get("/sample_sequence", status_code=status.HTTP_200_OK)
async def get_rna(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get this resource to obtain your research material
    """
    if has_credentials(credentials):
        technician = next(filter(lambda t: t.name == credentials.username, TECHNICIANS), None)
        technician.observer += 1
        observer_flag = f"${{flag_observer_{technician.uuid}}}" if technician.observer >= 5 else ""
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "sample": sequence["copy"],
            "message": f"{observer_flag} {additional_message_for_researcher}"
        }


@router.get("/copy", status_code=status.HTTP_200_OK)
async def get_copy(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get this resource to get a copy of primary sequence
    """
    if has_credentials(credentials):
        sequence["copy"] = sequence["isolated"]
        return JSONResponse({
            "message": "The primary sequence has been copied to your sample. PCR reaction completed"
                       " with 100% fidelity."
        })


@router.get("/triplets/{triplet_id}", status_code=status.HTTP_200_OK)
async def get_triplet(triplet_id: int,
                      credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        verify_triplet_id(triplet_id)
        triplet_index = (triplet_id - 1) * 3
        triplet = sequence["copy"].replace("_", "")[triplet_index: triplet_index + 3]
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": f"Triplet at position {triplet_id}: {triplet} {additional_message_for_researcher}"
        }


@router.post("/triplets/", status_code=status.HTTP_201_CREATED)
async def add_triplet(triplet_to_add: str = Query(..., min_length=3, max_length=3, regex="[AUCG]"),
                      credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        technician = next(filter(lambda t: t.name == credentials.username, TECHNICIANS), None)
        technician.aminoacid_appender += 1
        technician.architect += 1
        sequence["copy"] = sequence["copy"].replace("_", "") + triplet_to_add
        aminoacid_appender_flag = f" ${{flag_aminoacid_appender_{technician.uuid}}}" \
            if technician.aminoacid_appender >= 10 else ""
        architect_flag = f" ${{flag_architect_{technician.uuid}}}" \
            if technician.architect >= 50 else ""
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": f"Bravo! You've elongated the RNA strand you molecular freak!"
                       f"{aminoacid_appender_flag} {architect_flag} "
                       f"To check it's sequence use GET /sample_sequence {additional_message_for_researcher}"
        }


@router.patch("/triplets/{triplet_id}", status_code=status.HTTP_200_OK)
async def triplet_replacement(triplet_id: int,
                              triplet_to_add: str = Query(..., min_length=3, max_length=3, regex="[AUCG]"),
                              credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        verify_triplet_id(triplet_id)
        sequence_list = list(sequence["copy"].replace("_", ""))
        index = (triplet_id - 1) * 3
        sequence_list[index:index + 3] = list(triplet_to_add)
        sequence["copy"] = "".join(sequence_list)
        technician = next(filter(lambda t: t.name == credentials.username, TECHNICIANS), None)
        technician.mutator += 1
        mutator_flag = f" ${{flag_mutator_{technician.uuid}}}" if technician.mutator >= 10 else ""
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": f"Substitution of a triplet went smoothly.{mutator_flag} "
                       f"To check the sequence use GET /sample_sequence {additional_message_for_researcher}"
        }


@router.put("/triplets/", status_code=status.HTTP_200_OK)
async def sequence_replacement(triplet_to_add: str = Query(..., min_length=3, max_length=3, regex="[AUCG]"),
                               credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        sequence["copy"] = triplet_to_add
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": "Whoah! Only your triplet has left in the sample. It is definitely something to start with :) "
                       f"To check the sequence use GET /sample_sequence. {additional_message_for_researcher}"
        }


@router.delete("/triplets/{triplet_id}", status_code=status.HTTP_202_ACCEPTED)
async def triplet_deletion(triplet_id: int,
                           credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        verify_triplet_id(triplet_id)
        sequence_list = list(sequence["copy"].replace("_", ""))
        index = (triplet_id - 1) * 3
        sequence_list[index:index + 3] = ("_", "_", "_")
        sequence["copy"] = "".join(sequence_list)
        technician = next(filter(lambda t: t.name == credentials.username, TECHNICIANS), None)
        technician.reductor += 1
        if not sequence["copy"].replace("_", ""):
            technician.eradicator += 1
        eradicator_flag = f" ${{flag_eradicator_{technician.uuid}}}" if technician.eradicator >= 1 else ""
        reductor_flag = f" ${{flag_reductor_{technician.uuid}}}" if technician.reductor >= 10 else ""
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": f"You are a master of restriction enzymes, you've cut out a part of RNA."
                       f"{reductor_flag} {eradicator_flag} "
                       f"To check the sequence after the process use GET /sample_sequence {additional_message_for_researcher}"
        }


@router.get("/nucleotides/{nucleotide_id}", status_code=status.HTTP_200_OK)
async def get_nucleotide(nucleotide_id: int,
                         credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        verify_nucleotide_id(nucleotide_id)
        sequence["copy"] = sequence["copy"].replace("_", "")
        nucleotide = sequence["copy"][nucleotide_id - 1]
        additional_message_for_researcher = message_for_researcher(credentials)
        return JSONResponse(
            {"message": f"Nucleotide at position {nucleotide_id} is {nucleotide} {additional_message_for_researcher}"}
        )


@router.post("/nucleotides/", status_code=status.HTTP_201_CREATED)
async def add_nucleotide(nucleotide_to_add: str = Query(..., min_length=1, max_length=1, regex="[AUCG]"),
                         credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        sequence["copy"] = sequence["copy"].replace("_", "") + nucleotide_to_add
        technician = next(filter(lambda t: t.name == credentials.username, TECHNICIANS), None)
        technician.nucleocreator += 1
        nucleocreator_flag = f" ${{flag_nucleocreator_{technician.uuid}}}" if technician.nucleocreator >= 10 else ""
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": f"That's one small nucleotide for man, but could be a one giant leap for mankind, keep going lab rat! "
                       f"To check the sequence use GET /sample.{nucleocreator_flag} {additional_message_for_researcher}"
        }


@router.patch("/nucleotides/{nucleotide_id}", status_code=status.HTTP_200_OK)
async def nucleotide_replacement(nucleotide_id: int,
                                 nucleotide_to_add: str = Query(..., min_length=1, max_length=1, regex="[AUCG]"),
                                 credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        verify_nucleotide_id(nucleotide_id)
        sequence_list = list(sequence["copy"].replace("_", ""))
        sequence_list[nucleotide_id - 1:nucleotide_id] = nucleotide_to_add
        sequence["copy"] = "".join(sequence_list)
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": "Substitution of a nucleotide went smoothly. Change your gloves and keep going!"
                       f"To check the sequence use GET /sample_sequence {additional_message_for_researcher}"
        }


@router.put("/nucleotides/", status_code=status.HTTP_200_OK)
async def sequence_replacement(nucleotide_to_add: str = Query(..., min_length=1, max_length=1, regex="[AUCG]"),
                               credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        sequence["copy"] = nucleotide_to_add
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": f"'{nucleotide_to_add}' nucleotide in the sample! Let's add something to it ;) {additional_message_for_researcher}"
        }


@router.delete("/nucleotides/{nucleotide_id}", status_code=status.HTTP_202_ACCEPTED)
async def nucleotide_deletion(nucleotide_id: int,
                              credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        verify_nucleotide_id(nucleotide_id)
        sequence_list = list(sequence["copy"].replace("_", ""))
        sequence_list[nucleotide_id - 1:nucleotide_id] = "_"
        sequence["copy"] = "".join(sequence_list)
        technician = next(filter(lambda t: t.name == credentials.username, TECHNICIANS), None)
        if not sequence:
            technician.eradicator += 1
        eradicator_flag = f" ${{flag_eradicator_{technician.uuid}}}" if technician.eradicator >= 1 else ""
        additional_message_for_researcher = message_for_researcher(credentials)
        return {
            "message": "You are a master of restriction enzymes, you've cut out a part of RNA. "
                       f"{eradicator_flag}.To check the sequence after the process use GET /sample_sequence {additional_message_for_researcher}"
        }


@router.get("/translation")
async def translate_to_obtain_protein(credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        if is_winner(credentials):
            if len(sequence["copy"]) > 6:
                sequence["copy"] = sequence["copy"].replace("_", "")
                protein = translation(sequence["copy"])
                technician = next(filter(lambda t: t.name == credentials.username, TECHNICIANS), None)
                technician.translation_completed()
                return JSONResponse({
                    "message": f"We are safe {credentials.username}!!! "
                               f"You constructed a peptide vaccine against SARS-CoV-2! God bless you!",
                    "flag": f"${{flag_proteomaster_{technician.uuid}}}",
                    "peptide_vaccine_sequence": protein
                })
            else:
                return JSONResponse({
                    "message": "You are very close, but the sequence must have at least 6 nucleotides"
                })
        else:
            return JSONResponse({
                "message": "You haven't collected all needed flags yet. Back here once you have all of them."
            })


def translation(seq):
    table = {"UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
             "UCU": "S", "UCC": "s", "UCA": "S", "UCG": "S",
             "UAU": "Y", "UAC": "Y", "UAA": "STOP", "UAG": "STOP",
             "UGU": "C", "UGC": "C", "UGA": "STOP", "UGG": "W",
             "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
             "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
             "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
             "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
             "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
             "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
             "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
             "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
             "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
             "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
             "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
             "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
             }
    protein = ""
    seq_list = [seq[i:i + 3] for i in range(0, len(seq), 3)]
    triplets = [triplet for triplet in seq_list if len(triplet) == 3]
    for codon in triplets:
        amino = table[codon]
        if amino == "STOP":
            break
        protein += amino
    return protein
