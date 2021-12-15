import json
from datetime import datetime

import pytest

from app.api import crud, links


def test_create_link(test_app_with_db, monkeypatch):
    def mock_generate_link_list(link_id, url):
        return None

    monkeypatch.setattr(links, "generate_link_list", mock_generate_link_list)

    response = test_app_with_db.post(
        "/links/", data=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_links_invalid_json(test_app):
    response = test_app.post("/links/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = test_app.post("/links/", data=json.dumps({"url": "invalid://url"}))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_read_link(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://foo.bar",
        "sublinks": ["link"],
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/links/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_link_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/links/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "SubLinkList not found"


def test_read_all_links(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "https://foo.bar",
            "sublinks": ["link"],
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "url": "https://news.ycombinator.com",
            "sublinks": ["link"],
            "created_at": datetime.utcnow().isoformat(),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/links/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_link(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "url": "https://foo.bar",
            "sublinks": ["link"],
            "created_at": datetime.utcnow().isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/links/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": "https://foo.bar"}


def test_remove_link_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/links/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "SubLinkList not found"


def test_update_link(test_app, monkeypatch):
    test_request_payload = {"url": "https://foo.bar", "sublinks": ["updated"]}
    test_response_payload = {
        "id": 1,
        "url": "https://foo.bar",
        "sublinks": ["link"],
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        "/links/1/",
        data=json.dumps(test_request_payload),
    )
    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "link_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://foo.bar", "sublinks": ["updated!"]},
            404,
            "SubLinkList not found",
        ],
        [
            0,
            {"url": "https://foo.bar", "sublinks": ["updated!"]},
            422,
            [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "sublinks"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
        [
            1,
            {"url": "https://foo.bar"},
            422,
            [
                {
                    "loc": ["body", "sublinks"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        ],
    ],
)
def test_update_link_invalid(
    test_app, monkeypatch, link_id, payload, status_code, detail
):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(f"/links/{link_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_link_invalid_url(test_app):
    response = test_app.put(
        "/links/1/",
        data=json.dumps({"url": "invalid://url", "sublinks": ["updated!"]}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
