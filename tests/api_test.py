"""
API integration tests.
"""
from flask.testing import FlaskClient


def test_handle_user_event_when_event_doesnt_meet_alert_then_alert_flat_is_false(client: FlaskClient) -> None:
    input_data = {
        "type": "deposit",
        "amount": "100.00",
        "user_id": 11,
        "time": 0
    }

    expected_response = {
        "alert": False,
        "alert_codes": [],
        "user_id": 11
    }

    response = client.post("/event", json=input_data)

    assert response.status_code == 200
    assert response.json == expected_response


def test_handle_user_event_when_event_exceeds_limit_then_alert_flat_is_true(client: FlaskClient) -> None:
    input_data_1 = {
        "type": "deposit",
        "amount": "100.00",
        "user_id": 11,
        "time": 0
    }

    input_data_2 = {
        "type": "deposit",
        "amount": "101.00",
        "user_id": 11,
        "time": 3
    }

    expected_response_1 = {
        "alert": False,
        "alert_codes": [],
        "user_id": 11
    }

    expected_response_2 = {
        "alert": True,
        "alert_codes": [123],
        "user_id": 11
    }

    response_1 = client.post("/event", json=input_data_1)
    response_2 = client.post("/event", json=input_data_2)

    assert response_1.status_code == 200
    assert response_1.json == expected_response_1

    assert response_2.status_code == 200
    assert response_2.json == expected_response_2
