import pytest
import requests
from app.main import app
from unittest.mock import patch
from app.search import fetch_google_results, API_KEY 

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# 1) API_KEY is missing → RuntimeError
def test_missing_api_key(monkeypatch):
    monkeypatch.setattr("app.search.API_KEY", "")

    with pytest.raises(RuntimeError, match="SERPAPI_KEY"):
        fetch_google_results("python")


# 2)  Empty query → returns []
def test_empty_query(monkeypatch):
    monkeypatch.setattr("app.search.API_KEY", "test_api_key")
    assert fetch_google_results("") == []


# 3) Valid SerpAPI response → correct output structure
@patch("requests.get")
def test_valid_response(mock_get, monkeypatch):
    monkeypatch.setattr("app.search.API_KEY", "TEST_KEY")

    mock_get.return_value.json.return_value = {
        "organic_results": [
            {
                "title": "Python",
                "link": "https://python.org",
                "snippet": "Official Python website"
            }
        ]
    }
    mock_get.return_value.raise_for_status = lambda: None

    results = fetch_google_results("python")

    assert len(results) == 1
    assert results[0]["title"] == "Python"
    assert results[0]["link"] == "https://python.org"
    assert results[0]["snippet"] == "Official Python website"


# 5) SerpAPI error → raise_for_status should raise an exception
@patch("requests.get")
def test_serpapi_error(mock_get, monkeypatch):
    monkeypatch.setattr("app.search.API_KEY", "TEST_KEY")

    def raise_error():
        raise requests.HTTPError("SerpAPI error")

    mock_get.return_value.raise_for_status = raise_error

    with pytest.raises(requests.HTTPError):
        fetch_google_results("python")


# 6) Root endpoint (/) returns status 200
def test_index_page_status_200(client):
    response = client.get("/")
    assert response.status_code == 200


# 7) Missing query → API returns 400
def test_api_missing_query(client):
    response = client.get("/api/search")
    assert response.status_code == 400
    assert response.is_json
    assert response.get_json() == {
        "error": "Query is missing (parametr 'q')."
    }


