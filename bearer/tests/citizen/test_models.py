from ..client import test_client
from app.models import CitizenModel


def test_model():
    document = {
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
    CitizenModel(**document)