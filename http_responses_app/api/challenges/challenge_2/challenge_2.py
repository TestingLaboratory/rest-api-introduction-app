"""
Chernobyl Reactor
"""

from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from http_responses_app.api.challenges.challenge_2.model import CommanderCheckIn, Commander, ReactorCore, AZ5

router = APIRouter(prefix="/challenge/2")

commanders: List[Commander] = []
reactors: List[ReactorCore] = []


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"You are the Tech Commander of RBMK reactor power plant. "
                   f"check in at the /desk to get your key to control room. "
    }


@router.post("/desk", status_code=status.HTTP_201_CREATED)
async def check_in(commander_check_in: CommanderCheckIn):
    """
    Post your name to receive key to control room
    """
    if commander_check_in.name not in [c.name for c in commanders]:
        commander = Commander(commander_check_in.name)
        commanders.append(commander)
        reactors.append(ReactorCore(commander.uuid))
        return {
            "message": f"The key to your control room is {commander.uuid} ."
                       f"Keep it safe. use it as resource path to check on your RMBK-100 reactor!"
                       "use following: /{key}/control_room to gain knowledge how to operate reactor."
        }
    else:
        return JSONResponse(
            status_code=422,
            content={
                "message": "A spy?! That Power Plant Tech Leader has already checked in!"
            }
        )


@router.get("/{key}/control_room", status_code=status.HTTP_200_OK)
async def control_room(key: str):
    """
    Post your name to receive key to control room
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        return {
            "message": f"Hello {commander.uuid}",
            "reactor data": reactor
        }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "You're can't get pass this door comrade!"
            }
        )


@router.delete("/{key}/control_room/control_rods/{rod_number}", status_code=status.HTTP_202_ACCEPTED)
async def control_room(key: str, rod_number: int):
    """
    Use your key and rod number to remove given rod
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        result = reactor.remove_control_rod_at(rod_number)
        return {
            "message": f"Right, {commander.uuid}, {result}.",
        }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Lead! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.put("/{key}/control_room/control_rods/{rod_number}", status_code=status.HTTP_200_OK)
async def place_control_rod(key: str, rod_number: int):
    """
    Use your key and rod number to place given rod
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        result = reactor.add_control_rod_at(rod_number)
        return {
            "message": f"Right, Comrade {commander.uuid}, {result}.",
        }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Lead! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.put("/{key}/control_room/az_5", status_code=status.HTTP_200_OK)
async def manipulate_az_5(az_5_button: AZ5, key: str):
    """
    Use your key and PUT either true or false
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor and AZ5.pressed:
        result = reactor.press_AZ_5()
        if result == "BOOM!!!":
            return {
                "sound": result,
                "message": "Do you taste metal?!"
            }
        else:
            return {
                "message": f"Right, Comrade {commander.uuid}, {result}. "
                           f"Afraid of a meltdown, huh? ${{flag_cherenkov_chicken_{commander.name}}}"
            }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Lead! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.get("/{key}/reactor_core", status_code=status.HTTP_200_OK)
async def look_into_reactor_core(key: str):
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        if reactor.state != "BOOM!!!":
            return {
                "message": f"{commander.name}, the core looks fine!"
            }
        else:
            return {
                "message": "You've looked into radiating gates of hell..."
                           f"${{flag_death_from_acute_radiation_poisoning_{commander.name}}}"
            }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Lead! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.get("/{key}/control_room/analysis", status_code=status.HTTP_200_OK)
async def look_into_reactor_core(key: str):
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        if reactor.state == "Operational" and 1000< reactor.power < 1500:
            return {
                "message": f"{commander.name}! You have successfully completed the test!!! "
                f"General Secretary awards you ${{flag_plutonium_generator_{commander.name}}}!"
            }
        elif reactor.state != "BOOM!!!":
            return {
                "message": f"{commander.name}, the reactor is in state {reactor.state}! "
                f"It's power is on level {reactor.power}"
            }

    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Lead! Meddling with Power Plant! Get him to KGB!!!"
            }
        )

