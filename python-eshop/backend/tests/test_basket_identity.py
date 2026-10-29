from datetime import datetime, timedelta, timezone

from jose import jwt

from config import settings
from db.seed import DEMO_EMAIL
from tests.conftest import login


def basket_of(client, headers):
    return client.get("/api/basket", headers=headers).json()


def test_email_as_anonymous_basket_id_is_refused(client, demo_headers):
    attack = {"X-Basket-Id": DEMO_EMAIL}

    assert client.get("/api/basket", headers=attack).status_code == 400
    injected = client.post(
        "/api/basket/items",
        json={"catalog_item_id": 5, "quantity": 99},
        headers=attack,
    )
    assert injected.status_code == 400
    wiped = client.put("/api/basket/items", json={"quantities": {}}, headers=attack)
    assert wiped.status_code == 400

    assert basket_of(client, demo_headers)["item_count"] == 0


def test_malformed_anonymous_basket_id_is_refused(client):
    for bad in ["not-a-uuid", "12345", "' OR 1=1 --"]:
        response = client.get("/api/basket", headers={"X-Basket-Id": bad})
        assert response.status_code == 400, bad


def test_anonymous_basket_merges_on_login(client, anon_headers):
    client.post("/api/basket/items", json={"catalog_item_id": 2}, headers=anon_headers)

    headers = login(client, headers=anon_headers)

    basket = basket_of(client, headers)
    assert [item["catalog_item_id"] for item in basket["items"]] == [2]


def test_email_presented_at_login_does_not_move_another_basket(client):
    victim = login(client)
    client.post("/api/basket/items", json={"catalog_item_id": 1}, headers=victim)
    client.post(
        "/api/auth/register",
        json={"email": "attacker@example.com", "password": "secret123"},
        headers={"X-Basket-Id": DEMO_EMAIL},
    )

    assert basket_of(client, victim)["item_count"] == 1


def test_signed_in_shopper_can_manage_their_basket(client, demo_headers):
    basket = client.post(
        "/api/basket/items", json={"catalog_item_id": 4, "quantity": 2}, headers=demo_headers
    ).json()
    line = str(basket["items"][0]["id"])

    updated = client.put(
        "/api/basket/items", json={"quantities": {line: 3}}, headers=demo_headers
    ).json()
    assert updated["item_count"] == 3


def make_token(**overrides):
    payload = {"sub": DEMO_EMAIL, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
    payload.update(overrides)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def test_expired_token_is_rejected_not_downgraded(client, anon_headers):
    expired = make_token(exp=datetime.now(timezone.utc) - timedelta(minutes=1))
    headers = {**anon_headers, "Authorization": f"Bearer {expired}"}

    response = client.get("/api/basket", headers=headers)

    assert response.status_code == 401


def test_tampered_token_is_rejected(client, anon_headers):
    token = make_token()
    tampered = token[:-4] + ("AAAA" if not token.endswith("AAAA") else "BBBB")
    for value in [f"Bearer {tampered}", "Bearer not.a.token", "Basic abc"]:
        response = client.get(
            "/api/basket", headers={**anon_headers, "Authorization": value}
        )
        assert response.status_code == 401, value


def test_expired_token_is_rejected_on_orders(client):
    expired = make_token(exp=datetime.now(timezone.utc) - timedelta(minutes=1))

    response = client.get("/api/orders", headers={"Authorization": f"Bearer {expired}"})

    assert response.status_code == 401


def test_no_token_still_shops_anonymously(client, anon_headers):
    assert client.get("/api/basket", headers=anon_headers).status_code == 200


def test_basket_survives_an_expired_session(client, demo_headers):
    client.post("/api/basket/items", json={"catalog_item_id": 6}, headers=demo_headers)

    headers = login(client)

    assert basket_of(client, headers)["item_count"] == 1
