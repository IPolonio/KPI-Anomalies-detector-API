from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="KPI Anomaly detection API")

class KPI_record(BaseModel):
    label: str
    revenue: float 
    orders: int 
    conversion_rate: float 
    
    
class KPI_batch(BaseModel):
    records : list[KPI_record]




@app.get("/")
def health():
    return  {"Service":"KPI anomaly detection API","Status":"Healthy"}

@app.post("/rule-check")
def rule_checks(batch : KPI_batch):
    results = []
    
    for record in batch.records:
        is_anomaly = (
            record.revenue < 500
            or record.revenue > 5000
            or record.orders < 10
            or record.orders > 200
            or record.conversion_rate < 0.01
            or record.conversion_rate > 0.10
        )
        results.append({"label": record.label,"is_anomaly" : is_anomaly})
    return {"method": "fixed threshold", "result":results }

     