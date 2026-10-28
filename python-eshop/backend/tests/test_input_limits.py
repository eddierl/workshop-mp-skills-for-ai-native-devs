import pytest

from tests.conftest import login

LIMIT = 99


def register(client, password, email="limits@example.com"):
    return client.post("/api/auth/register", json={"email": email, "password": password})


def test_over_long_password_is_refused_with_a_clear_message(client):
    response = register(client, "x" * 90)

    assert response.status_code == 422
    message = str(response.json()["detail"])
    assert "72" in message
    assert "truncate" not in message


def test_multibyte_password_over_72_bytes_is_refused(client):
    assert register(client, "é" * 40).status_code == 422


@pytest.mark.parametrize("length", [71, 72])
def test_passwords_at_the_limit_still_work(client, length):
    password = "p" * length
    email = f"len{length}@example.com"

    assert register(client, password, email).status_code == 200
    login(client, email, password)


def test_over_long_password_at_login_is_just_wrong(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "demouser@perthai.com.au", "password": "x" * 200},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def add(client, headers, quantity, item=1):
    return client.post(
        "/api/basket/items",
        json={"catalog_item_id": item, "quantity": quantity},
        headers=headers,
    )


def test_quantity_above_the_limit_is_refused(client, anon_headers):
    assert add(client, anon_headers, 1_000_000_000).status_code == 422
    assert add(client, anon_headers, LIMIT + 1).status_code == 422
    assert add(client, anon_headers, LIMIT).status_code == 200


def test_adding_cannot_push_a_line_over_the_limit(client, anon_headers):
    add(client, anon_headers, LIMIT - 1)

    response = add(client, anon_headers, 5)

    assert response.status_code == 400
    assert str(LIMIT) in response.json()["detail"]


def test_bulk_update_enforces_the_same_bounds(client, anon_headers):
    basket = add(client, anon_headers, 2).json()
    line = str(basket["items"][0]["id"])

    def put(quantity):
        return client.put(
            "/api/basket/items", json={"quantities": {line: quantity}}, headers=anon_headers
        )

    assert put(LIMIT + 1).status_code == 422
    assert put(-1).status_code == 422
    assert put(LIMIT).json()["item_count"] == LIMIT
    assert put(0).json()["items"] == []
