import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from API import app


client = TestClient(app)


def test_health_endpoint_returns_healthy_status():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Service": "KPI anomaly detection API", "Status": "Healthy"}


def test_rule_check_flags_records_inside_and_outside_thresholds():
    payload = {
        "records": [
            {
                "label": "normal",
                "revenue": 1200.0,
                "orders": 40,
                "conversion_rate": 0.05,
            },
            {
                "label": "anomalous",
                "revenue": 300.0,
                "orders": 8,
                "conversion_rate": 0.2,
            },
        ]
    }

    response = client.post("/rule-check", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "method": "fixed threshold",
        "result": [
            {"label": "normal", "is_anomaly": False},
            {"label": "anomalous", "is_anomaly": True},
        ],
    }
