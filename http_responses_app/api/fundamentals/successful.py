from faker import Faker
from faker.providers import person
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from http_responses_app.core.responses import get_response, post_response, put_response
from http_responses_app.model.pong import Pong

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
    return _people


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
        guys_and_gals = list(filter(lambda someone: someone["first_name"].lower() == first_name.lower(), guys_and_gals))
    if last_name:
        guys_and_gals = list(filter(lambda someone: someone["last_name"].lower() == last_name.lower(), guys_and_gals))

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


@router.post("/created")
async def post_response_201(request: Pong):
    return post_response(201, request)


@router.put("/created")
async def put_response_201(request: Pong):
    return put_response(201, request)
