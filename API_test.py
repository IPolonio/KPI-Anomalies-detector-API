import json
from pathlib  import Path

from fastapi.testclient import TestClient

from API import app

client = TestClient(app)


Sample = json.loads(
    (Path(__file__).parent/"sample-request.json").read_text(encoding="utf-8")
)


def test_health_endpoint():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json()["Status"] == "Healthy"
    
    
def test_isolation_forest_detects():
    response = client.post("/detect",json=Sample)
    
    assert response.status_code == 200
    results = response.json()["results"]
    campaign_spike = next(
    item for item in results if item["label"] == "campaign-spike"
    )
    assert campaign_spike["is_anomaly"] is True
    assert sum(item["is_anomaly"] for item in results) == 1