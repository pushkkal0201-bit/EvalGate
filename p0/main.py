from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import make_asgi_app

app = FastAPI(title="EvalGate")
app.mount("/metrics", make_asgi_app())

@app.get("/health")
def health():
    return {"status":"ok","service":"EvalGate"}

class Request(BaseModel):
    baseline: float = Field(ge=0,le=1)
    candidate: float = Field(ge=0,le=1)
    estimated_cost: float = Field(ge=0)
    budget: float = Field(ge=0)

@app.post("/v1/gate")
def gate(body: Request):
    return {"passed":body.candidate>=body.baseline and body.estimated_cost<=body.budget}

from core import evaluate

class Case(BaseModel):
    expected: str = Field(max_length=4096)
    actual: str = Field(max_length=4096)

class Dataset(BaseModel):
    cases: list[Case] = Field(min_length=1,max_length=1000)

@app.post("/v1/evaluate")
def evaluation(body: Dataset):
    return evaluate([case.model_dump() for case in body.cases])
