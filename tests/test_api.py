from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health_endpoint_returns_basic_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["loaded_models"] >= 1


def test_predict_unknown_category_returns_not_found() -> None:
    response = client.post(
        "/predict",
        json={
            "category": "UnknownCategory",
            "sku": "SKU-001",
            "date": "2026-04-01",
            "price_unit": 120.0,
            "promotion_flag": 0,
            "stock_available": 200,
            "delivery_days": 3,
        },
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_insights_unknown_category_returns_not_found() -> None:
    response = client.get("/insights/UnknownCategory")

    assert response.status_code == 404
    assert "no model" in response.json()["detail"].lower()
