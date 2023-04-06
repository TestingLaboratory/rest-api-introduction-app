"""
Chernobyl Reactor
"""
from typing import List

from fastapi import APIRouter, Header
from starlette import status
from starlette.responses import JSONResponse
from unidecode import unidecode

from rest_introduction_app.api.challenges.challenge_2.model import CommanderCheckIn, Commander, ReactorCore, AZ5, Purge

challenge_prefix = "/challenge/reactor"
challenge_tag = "Challenge - RBMK Reactor test"
router = APIRouter(prefix=challenge_prefix)

commanders: List[Commander] = []
reactors: List[ReactorCore] = []




@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information(
        for_frontend: str = Header(default=None, convert_underscores=True, include_in_schema=False)
):
    """
    Get this resource to obtain mission debrief
    """
    # TODO create a single object for each flags_to_find
    flags_to_find = 12
    if for_frontend == "only":
        return {
            "message": f"You are the Tech Commander of RBMK reactor power plant. "
                       f"Your task is to perform the reactor test. "
                       f"Bring the power level above 1200 but below 1500 and keep the reactor Operational. "
                       f"Don't forget to pick up the key on your way up. "
                       f"Put in fuel rods or pull out control rods to raise the power. "
                       f"Put in control rods or pull out fuel rods to decrease the power. "
                       f"Good luck Commander. ",
            "flagsToFind": flags_to_find
        }
    else:
        return {
            "message": f"You are the Tech Commander of RBMK reactor power plant. "
                       f"Your task is to perform the reactor test. "
                       f"Bring the power level above 1200 but below 1500 and keep the reactor Operational. "
                       f"Use /{{key}}/control_room/analysis to peek at reactor core. "
                       f"Use /{{key}}/control_room to see full info about the reactor. "
                       f"Check in at the /desk to get your key to control room. "
                       f"Put in fuel rods or pull out control rods to raise the power. "
                       f"Put in control rods or pull out fuel rods to decrease the power. "
                       f"There are {flags_to_find} flags to find. "
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
                       f"Keep it safe. use it as resource path to check on your RBMK-1000 reactor! "
                       "Use following: /{key}/control_room to gain knowledge how to operate reactor. "
                       "You may see if the core is intact here: /{key}/reactor_core . "
                       "If anything goes wrong push AZ-5 safety button to put all control rods in place!"
                       " Good luck Commander.",
            "key": f"{commander.uuid}"
        }
        response = JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=content
        )
        response.set_cookie("secret_documentation",
                            "Reactor will blow up if it is poisoned, overpowered and you press AZ5"
                            "${flag_keeper_of_secrets}")
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
            "message": f"Hello, Comrade {commander.name}. What would you like to see?",
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
        if reactor.state == "BOOM!!!":
            return JSONResponse(
                status_code=409,
                content={"message": "Something's wrong... It's not working..."}
            )
        result = reactor.remove_control_rod_at(rod_number)
        if "Removing control rod" in result:
            commander.control_rod_manipulation += 1
        manipulator_flag = "${flag_control_rod_manipulator}" if \
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
        if reactor.state == "BOOM!!!":
            return JSONResponse(
                status_code=409,
                content={
                    "message": "Something's wrong... It's not working...",
                    "flag": "${couldn't_lower_the_rods_into_the_core_because_there's_no_core!}"
                }
            )
        result = reactor.add_control_rod_at(rod_number)
        if "Adding control rod" in result:
            commander.control_rod_manipulation += 1
        manipulator_flag = "${flag_control_rod_manipulator}" if \
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
                "message": "Do you taste metal?!",
                "flag": "${flag_dead_in_two_weeks}"
            }
        else:
            return JSONResponse(
                status_code=425,
                content={
                    "message": f"Right, Comrade {commander.name}, Reactor State is: {result}. "
                               "Afraid of a meltdown, huh?",
                    "flag": "${flag_cherenkov_chicken}"
                }
            )
    elif commander and reactor and not az_5_button.pressed:
        return JSONResponse(
            status_code=400,
            content={
                "message": "So... How do you >unpress< the button? I mean... Is it even possible?"
            }
        )
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
                "flag": "${flag_curious_aren't_we}"
            }
        else:
            return {
                "message": "You've looked into radiating gates of hell...",
                "flag": "${flag_death_from_acute_radiation_poisoning}"
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
        if reactor.state == "Operational" and 1200 < reactor.power < 1500:
            return {
                "message": f"{commander.name}! You have successfully completed the test!!! "
                           f"General Secretary awards you!",
                "flag": " ${flag_plutonium_generator}"
            }
        elif reactor.state != "BOOM!!!":
            return {
                "message": f"{commander.name.title()},"
                           f" the reactor '{reactor.description}' is in state {reactor.state}! "
                           f"It's power is on level {reactor.power}"
            }
        else:
            return {
                "message": f"Run and check the reactor core!!!"
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
        if reactor.state == "BOOM!!!":
            return JSONResponse(
                status_code=409,
                content={"message": "Something's wrong... It's not working..."}
            )
        result = reactor.remove_fuel_rod_at(rod_number)
        if "Removing fuel rod" in result:
            commander.fuel_rod_manipulation += 1
        manipulator_flag = "${flag_fuel_rod_manipulator}" if \
            commander.fuel_rod_manipulation > 50 else None
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
        if reactor.state == "BOOM!!!":
            return JSONResponse(
                status_code=409,
                content={"message": "Something's wrong... It's not working..."}
            )
        result = reactor.add_fuel_rod_at(rod_number)
        if "Adding fuel rod" in result:
            commander.fuel_rod_manipulation += 1
        manipulator_flag = "${flag_fuel_rod_manipulator}" if \
            commander.fuel_rod_manipulation > 50 else None
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
                "flag": "${flag_you_didn't_see_the_graphite_because_it's_not_there}"
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Who are you?!",
                "flag": "${flag_what_is_the_cost_of_lies}"
            }
        )


@router.get("/check_key/{key}", status_code=status.HTTP_200_OK, include_in_schema=False)
async def check_key(key: str):
    if next(filter(lambda c: c.uuid == key, commanders), None):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "You can now proceed with the timeline reversal process.",
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Wrong key... Are you sure you know where you are? This is classified area.",
            }
        )


@router.get("/clear_everything", status_code=status.HTTP_200_OK, include_in_schema=False)
async def clear_everything():
    """
    Method to clear all data when called - to reset for another training group
    """
    global commanders

    return {
        "message": "To be Purged",
        "commanders": commanders
    }


@router.post("/clear_everything", include_in_schema=False)
async def clear_everything(purge: Purge):
    """
    Method to clear all data when called - to reset for another training group
    """
    global commanders, reactors
    commanders = []
    reactors = []
    if purge.purge:
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "message": "Purged everything",
                "commanders": commanders,
                "reactors": reactors,
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "message": "Nope.",
            }
        )
