import faker
from faker import Faker
from fastapi.testclient import TestClient

from rest_introduction_app.reactor_challenge import app

client = TestClient(app)
fake = Faker()
PATH = 'challenge/reactor'

information_message = 'You are the Tech Commander of RBMK reactor power plant. Your task ' + \
                      'is to perform the reactor test. Bring the power level above 1000 ' + \
                      'but below 1500 and keep the reactor Operational. Use ' + \
                      '/{key}/control_room/analysis to peek at reactor core. Use ' + \
                      '/{key}/control_room to see full info about the reactor. Check in ' + \
                      'at the /desk to get your key to control room. Put in fuel rods or ' + \
                      'pull out control rods to raise the power. Put in control rods or ' + \
                      'pull out fuel rods to decrease the power. There are 11 flags to ' + \
                      'find. Good luck Commander. '


def test_information():
    response = client.get(f"{PATH}/information")
    assert response.status_code == 200
    assert response.json() == {'message': information_message}

def test_check_in():
    payload = {
        "name": fake.name()
    }
    response = client.post(f"{PATH}/desk", json=payload)
    assert response.status_code == 201
    assert response.json().get('key')
    assert response.json().get('message') == 'Take the key to your control room. Keep it safe. use it as \n' \
                                             'resource path to check on your RBMK-1000 reactor! Use following: ' \
                                             '/{key}/control_room to gain knowledge how to operate reactor.' \
                                             ' You may see if the core is intact here: /{key}/reactor_core . If ' \
                                             'anything goes wrong push AZ-5 safety button to put all control ' \
                                             'rods in place! Good luck Commander.'