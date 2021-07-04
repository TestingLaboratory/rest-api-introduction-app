"""
Chernobyl Reactor
"""
from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_2.model import CommanderCheckIn, Commander, ReactorCore, AZ5
from unidecode import unidecode

challenge_prefix = "/challenge/reactor"
challenge_tag = "Challenge - RBMK Reactor test"
router = APIRouter(prefix=challenge_prefix)

commanders: List[Commander] = []
reactors: List[ReactorCore] = []


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"You are the Tech Commander of RBMK reactor power plant. "
                   f"Your task is to perform the reactor test. "
                   f"Bring the power level above 1000 but below 1500 and keep the reactor Operational. "
                   f"Use /{{key}}/control_room/analysis to peek at reactor core. "
                   f"Use /{{key}}/control_room to see full info about the reactor. "
                   f"Check in at the /desk to get your key to control room. "
                   f"Put in fuel rods or pull out control rods to raise the power. "
                   f"Put in control rods or pull out fuel rods to decrease the power. "
                   f"There are 12 flags to find. "
                   f"Good luck Commander. "
    }


@router.post("/desk", status_code=status.HTTP_201_CREATED)
async def check_in(commander_check_in: CommanderCheckIn):
    """
    Post your name to receive key to control room
    """
    name = unidecode(commander_check_in.name)
    if name not in [c.name for c in commanders]:
        commander = Commander(name)
        commanders.append(commander)
        reactors.append(ReactorCore(commander.uuid))
        content = {
            "message": f"Take the key to your control room. "
                       f"Keep it safe. use it as resource path to check on your RMBK-100 reactor! "
                       "Use following: /{key}/control_room to gain knowledge how to operate reactor. "
                       "You may see if the core is intact here: /{key}/reactor_core . "
                       "If anything goes wrong push AZ-5 safety button to put all control rods in place!"
                       "Good luck Commander.",
            "key": f"{commander.uuid}"
        }
        response = JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=content
        )
        response.set_cookie("secret_documentation",
                            "Reactor will blow up if it is poisoned, overpowered and you press AZ5"
                            f"${{flag_keeper_of_secrets_{commander.name}}}")
        return response
    else:

        return JSONResponse(
            status_code=422,
            content={
                "message": "A spy?! That Power Plant Tech Commander has already checked in!"
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
            "message": f"Hello {commander.name}",
            "reactor data": reactor
        }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "You're can't get pass this door comrade! ${flag_sneaky_rat}"
            }
        )


@router.delete("/{key}/control_room/control_rods/{rod_number}", status_code=status.HTTP_202_ACCEPTED)
async def control_rod_delete(key: str, rod_number: int):
    """
    Use your key and rod number to remove given rod
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        result = reactor.remove_control_rod_at(rod_number)
        commander.control_rod_manipulation += 1
        manipulator_flag = f"${{flag_control_rod_manipulator_{commander.name}}}" if \
            commander.control_rod_manipulation > 30 else None
        response = {
            "message": f"Right, {commander.name}, {result}.",
        }
        if manipulator_flag:
            response.update({"flag": manipulator_flag})
        return response
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Commander! Meddling with Power Plant! Get him to KGB!!!"
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
        commander.control_rod_manipulation += 1
        manipulator_flag = f"${{flag_control_rod_manipulator_{commander.name}}}" if \
            commander.control_rod_manipulation > 30 else None
        response = {
            "message": f"Right, {commander.name}, {result}.",
        }
        if manipulator_flag:
            response.update({"flag": manipulator_flag})
        return response
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Commander! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.put("/{key}/control_room/az_5", status_code=status.HTTP_200_OK)
async def manipulate_az_5(az_5_button: AZ5, key: str):
    """
    Use your key and PUT either true or false
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor and az_5_button.pressed:
        result = reactor.press_az_5()
        if result == "BOOM!!!":
            return {
                "sound": result,
                "message": f"Do you taste metal?!",
                "flag": f"${{flag_dead_in_two_weeks_{commander.name}}}"
            }
        else:
            return {
                "message": f"Right, Comrade {commander.name}, {result}. "
                           f"Afraid of a meltdown, huh?",
                "flag": f"${{flag_cherenkov_chicken_{commander.name}}}"
            }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Commander! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.get("/{key}/reactor_core", status_code=status.HTTP_200_OK)
async def look_into_reactor_core(key: str):
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        if reactor.state != "BOOM!!!":
            return {
                "message": f"{commander.name}, the core looks fine!",
                "flag": f"${{flag_curious_arent_we_{commander.name}}}"
            }
        else:
            return {
                "message": "You've looked into radiating gates of hell...",
                "flag": f"${{flag_death_from_acute_radiation_poisoning_{commander.name}}}"
            }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Commander! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.get("/{key}/control_room/analysis", status_code=status.HTTP_200_OK)
async def analysis(key: str):
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        if reactor.state == "Operational" and 1000 < reactor.power < 1500:
            return {
                "message": f"{commander.name}! You have successfully completed the test!!! "
                           f"General Secretary awards you!",
                "flag": f" ${{flag_plutonium_generator_{commander.name}}}"
            }
        elif reactor.state != "BOOM!!!":
            return {
                "message": f"{commander.name}, the reactor is in state {reactor.state}! "
                           f"It's power is on level {reactor.power}"
            }
        else:
            return {
                "message": f"Run and check the reactor core!!! /{commander.uuid}/reactor_core"
            }
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Commander! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.delete("/{key}/control_room/fuel_rods/{rod_number}", status_code=status.HTTP_202_ACCEPTED)
async def remove_fuel_rod(key: str, rod_number: int):
    """
    Use your key and rod number to remove given rod
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        result = reactor.remove_fuel_rod_at(rod_number)
        commander.fuel_rod_manipulation += 1
        manipulator_flag = f"${{flag_fuel_rod_manipulator_{commander.name}}}" if \
            commander.fuel_rod_manipulation > 30 else None
        response = {
            "message": f"Right, {commander.name}, {result}.",
        }
        if manipulator_flag:
            response.update({"flag": manipulator_flag})
        return response
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Commander! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.put("/{key}/control_room/fuel_rods/{rod_number}", status_code=status.HTTP_200_OK)
async def place_fuel_rod(key: str, rod_number: int):
    """
    Use your key and rod number to place given rod
    """
    commander = next(filter(lambda c: c.uuid == key, commanders), None)
    reactor = next(filter(lambda r: r.uuid == key, reactors), None)
    if commander and reactor:
        result = reactor.add_fuel_rod_at(rod_number)
        commander.fuel_rod_manipulation += 1
        manipulator_flag = f"${{flag_fuel_rod_manipulator_{commander.name}}}" if \
            commander.fuel_rod_manipulation > 30 else None
        response = {
            "message": f"Right, {commander.name}, {result}.",
        }
        if manipulator_flag:
            response.update({"flag": manipulator_flag})
        return response
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "He's not a Tech Commander! Meddling with Power Plant! Get him to KGB!!!"
            }
        )


@router.get("/{key}/reset_progress")
async def reset_progress(key: str):
    if commander := next(filter(lambda c: c.uuid == key, commanders), None):
        commander = Commander(commander.name)
        reactor_index = reactors.index(ReactorCore(commander.uuid))
        reactors[reactor_index] = ReactorCore(commander.uuid)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Your reactor is good as new!",
                "flag": "${flag_you_didnt_see_the_graphite_because_its_not_there}"
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "No such Commander!",
                "flag": "${flag_atomna_elektrostancja_erector}"
            }
        )
