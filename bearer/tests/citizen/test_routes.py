from app.models import citizen_model
from app.models.citizen_model import CitizenMailAuth
from ..client import test_client
from requests.auth import HTTPBasicAuth
from app.models import CitizenModel
import json
paul_document = {
    "name" : "john",
    "surname" : "paul",
    "PID" : "12345678911",
    "ID_card_number" : "11111111111",
    "martial_status" : "lenny face",
    "driver_license_id" : "0123456789A",
    "driver_license_exp_date" : "2222-01-21",
    "driver_penalty_points" : "10",
    "place_of_birth" : "Warsaw",
    "residence" : "Gdynia",
    "contact_number" : "123456789",
    "contact_mail" : "examplemail@mail.com"
}

mail_doc ={
    "name" : "john",
    "surname" : "paul",
    "PID" : "12345678911",
    "contact_mail" : "examplemail@mail.com"
}

def mock_database(mocker):
    async def mocked_read(cit_id):
        assert cit_id == paul_document["PID"], "router had modified the internal value!!!"
        return CitizenModel(**paul_document)

    async def mocked_create(cit_model):
        document_in_string = json.dumps(paul_document)
        assert type(cit_model.json()) == type(document_in_string)
        assert cit_model.json() == document_in_string
        return True

    async def mocked_mail(cit_id):
        return True

    async def mocked_delete(cit_id):
        return True

    mocker.patch(
        "app.db.citizen.read_citizen",
        side_effect=mocked_read
    )

    mocker.patch(
        "app.db.citizen.create_citizen",
        side_effect=mocked_create
    )

    mocker.patch(
        "app.db.citizen.update_mail",
        side_effect=mocked_mail
    )

    mocker.patch(
        "app.db.citizen.delete_citizen",
        side_effect=mocked_delete
    )


def test_route_get(mocker):
    mock_database(mocker)
    auth = HTTPBasicAuth(username="Pierwszy urzad skarbowy", password="haslo")
    response = test_client.get("/citizen", auth=auth, params={"citizen_id": "12345678911"})
    assert response.json() == paul_document


def test_route_post(mocker):
    mock_database(mocker)
    auth = HTTPBasicAuth(username="Pierwszy urzad skarbowy", password="haslo")
    response = test_client.post("/citizen", auth=auth, params={"citizen_id": "12345678911"}, json=paul_document)
    assert response.json() == {"success" : True}

def test_route_put(mocker):
    ...

def test_route_delete(mocker):
    ...
