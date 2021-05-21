from faker import Faker
from faker.providers import person
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from rest_introduction_app.api.fundamentals.core.responses import get_response, post_response, put_response
from rest_introduction_app.api.fundamentals.model.pong import Pong

router = APIRouter()

_fake = Faker(locale="pl_PL")
_fake.add_provider(person)
_people = [{"first_name": _fake.first_name(),
            "last_name": _fake.last_name()}
           for _ in range(1000)]


@router.get("/ok")
async def get_response_200():
    return get_response(200)


@router.get("/query_params")
async def get_response_200_params(first_name, last_name, middle_name=None, height: int = None):
    height = f" Your height is: {height}" if height else ""
    person_to_greet = f"{first_name}{f' {middle_name} ' if middle_name else ' '}{last_name}"
    return {
        "Greeting": f"Hello, {person_to_greet}!{height}"
    }


@router.get("/get_all_people")
async def get_people():
    """
    Endpoint to get all people
    :return:
    """
    return {index: human for index, human in enumerate(_people)}


@router.get("/get_all_people_sliced")
async def get_people(from_number: int = None, up_to_number: int = None):
    """
    Endpoint to get all people from-to given number
    :return: list of people from-to numbers
    """
    return _people[from_number:up_to_number]


@router.get("/get_all_people_paged")
async def get_people(page_size: int, page_number: int = 0):
    """
    Endpoint to get all people
    :return: list of people by pages using given page size
    """
    return _people[page_size * page_number:page_size * (page_number + 1)]


@router.get("/get_people_by")
async def get_people_params(first_name=None, last_name=None):
    """
    Endpoint to search for people by names
    :return: list of people by pages using given page size
    """
    guys_and_gals = _people[:]
    if first_name:
        guys_and_gals = list(filter(lambda someone: someone.get("first_name", "").lower() == first_name.lower(),
                                    guys_and_gals))
    if last_name:
        guys_and_gals = list(filter(lambda someone: someone.get("last_name", "").lower() == last_name.lower(),
                                    guys_and_gals))

    if (first_name or last_name) and guys_and_gals:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=guys_and_gals
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No such person exists."}
        )


@router.post("/human/")
async def post_response_201(body: dict):
    """
    Body should have at least first_name, and last_name as keys in json in body    :param body:
    """
    _people.append(body)
    return JSONResponse(content={
        "message": f"Human {_people[-1]} created at index {len(_people) - 1}"
    },
        status_code=status.HTTP_201_CREATED)


@router.put("/human/{human_id}")
async def put_response_202(body: dict, human_id: int):
    """
    Body should have at least first_name, and last_name as keys in json in body
    """
    try:
        _people[human_id] = body
        return JSONResponse(content={
            "message": f"Human at index {human_id} modified as follows",
            "human": _people[human_id]},
            status_code=status.HTTP_202_ACCEPTED)
    except IndexError:
        return JSONResponse(content={
            "message": "Excuse me, whaaaat?!"},
            status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/human/{human_id}")
async def patch_human(body: dict, human_id: int):
    """
    Body should have at least first_name, and last_name as keys in json in body
    """
    try:
        _people[human_id].update(body)
        return JSONResponse(content={
            "message": f"Human at index {human_id} modified as follows",
            "human": _people[human_id]},
            status_code=status.HTTP_202_ACCEPTED)
    except IndexError:
        return JSONResponse(content={
            "message": "Excuse me, whaaaat?!"},
            status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/human/{human_id}")
async def delete_human(human_id: int):
    try:
        _people[human_id] = dict()
        return JSONResponse(content={
            "message": f"Human at index {human_id} deleted.",
            "human": _people[human_id]},
            status_code=status.HTTP_202_ACCEPTED)
    except IndexError:
        return JSONResponse(content={
            "message": "Excuse me, whaaaat?!"},
            status_code=status.HTTP_404_NOT_FOUND)


@router.get("/human/{human_id}")
async def get_human(human_id: int):
    """
    Body should have at least first_name, and last_name as keys in json in body
    """
    try:
        return JSONResponse(content={
            "message": f"Human at index {human_id} looks as follows",
            "human": _people[human_id]},
            status_code=status.HTTP_200_OK)
    except IndexError:
        return JSONResponse(content={
            "message": "Excuse me, whaaaat?!"},
            status_code=status.HTTP_404_NOT_FOUND)
