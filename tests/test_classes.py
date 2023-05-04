from datetime import datetime

import pytest
from pydantic import ValidationError

from webapi.backend.classes import Client
from webapi.backend.classes import Policies
from webapi.backend.classes import Role


def test_role_enum():
    assert Role.admin == "admin"
    assert Role.user == "user"
    assert Role.guest == "guest"

    with pytest.raises(ValueError):
        Role("invalid_role")


def test_client_validation():
    valid_client = {
        "id": "1",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "role": "admin",
    }
    client = Client(**valid_client)
    assert client.dict() == valid_client

    invalid_client = {
        "id": "2",
        "name": "",
        "email": 12345,  # Invalid type
        "role": "invalid_role",
    }
    with pytest.raises(ValidationError):
        Client(**invalid_client)


def test_policies_validation():
    valid_policies = {
        "id": "1",
        "amountInsured": 1000.0,
        "email": "johndoe@example.com",
        "inceptionDate": datetime.fromisoformat("2022-01-01T00:00:00"),
        "installmentPayment": True,
        "clientId": "1",
    }
    policies = Policies(**valid_policies)
    assert policies.dict() == valid_policies

    invalid_policies = {
        "id": "2",
        "amountInsured": -1000.0,
        "email": "not_an_email",
        "inceptionDate": "invalid_date",
        "installmentPayment": "not_a_boolean",
        "clientId": "",
    }
    with pytest.raises(ValidationError):
        Policies(**invalid_policies)
