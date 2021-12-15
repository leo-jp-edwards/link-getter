import json

import pytest

from app.api import links


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


def test_read_link(test_app_with_db, monkeypatch):
    def mock_generate_link_list(link_id, url):
        return None

    monkeypatch.setattr(links, "generate_link_list", mock_generate_link_list)

    response = test_app_with_db.post(
        "/links/", data=json.dumps({"url": "https://foo.bar"})
    )
    link_id = response.json()["id"]

    response = test_app_with_db.get(f"/links/{link_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == link_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["sublinks"] is not None
    assert response_dict["created_at"] is not None


def test_read_link_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/links/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "SubLinkList not found"

    response = test_app_with_db.get("/links/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_read_all_links(test_app_with_db, monkeypatch):
    def mock_generate_link_list(link_id, url):
        return None

    monkeypatch.setattr(links, "generate_link_list", mock_generate_link_list)

    response = test_app_with_db.post(
        "/links/", data=json.dumps({"url": "https://foo.bar"})
    )
    link_id = response.json()["id"]

    response = test_app_with_db.get("/links/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == link_id, response_list))) == 1


def test_remove_link(test_app_with_db, monkeypatch):
    def mock_generate_link_list(link_id, url):
        return None

    monkeypatch.setattr(links, "generate_link_list", mock_generate_link_list)

    response = test_app_with_db.post(
        "/links/", data=json.dumps({"url": "https://foo.bar"})
    )
    link_id = response.json()["id"]

    response = test_app_with_db.delete(f"/links/{link_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": link_id, "url": "https://foo.bar"}


def test_remove_link_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/links/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "SubLinkList not found"

    response = test_app_with_db.delete("/links/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_link(test_app_with_db, monkeypatch):
    def mock_generate_link_list(link_id, url):
        return None

    monkeypatch.setattr(links, "generate_link_list", mock_generate_link_list)

    response = test_app_with_db.post(
        "/links/", data=json.dumps({"url": "https://foo.bar"})
    )
    link_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/links/{link_id}/",
        data=json.dumps({"url": "https://foo.bar", "sublinks": ["updated!"]}),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == link_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["sublinks"] == ["updated!"]
    assert response_dict["created_at"]


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
def test_update_link_invalid(test_app_with_db, link_id, payload, status_code, detail):
    response = test_app_with_db.put(f"/links/{link_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_link_invalid_url(test_app):
    response = test_app.put(
        "/links/1/",
        data=json.dumps({"url": "invalid://url", "sublinks": ["updated!"]}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
