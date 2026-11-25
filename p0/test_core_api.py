from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_evaluation():
    result=client.post("/v1/evaluate",json={"cases":[{"expected":"yes","actual":" YES "},{"expected":"no","actual":"yes"}]}).json()
    assert result["exact_match"]==0.5

def test_budget_gate():
    assert client.post("/v1/gate",json={"baseline":0.8,"candidate":0.9,"estimated_cost":11,"budget":10}).json()["passed"] is False
