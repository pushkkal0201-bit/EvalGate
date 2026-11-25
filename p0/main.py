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

from advanced import cosine_similarity, regression
from fastapi import HTTPException

class SimilarityRequest(BaseModel):
    a: list[float] = Field(min_length=1,max_length=4096)
    b: list[float] = Field(min_length=1,max_length=4096)

@app.post("/v1/similarity")
def similarity(body: SimilarityRequest):
    try:
        return {"similarity":cosine_similarity(body.a,body.b)}
    except ValueError as exc:
        raise HTTPException(422,str(exc))

class RegressionRequest(BaseModel):
    baseline: float = Field(ge=0,le=1)
    candidate: float = Field(ge=0,le=1)
    tolerance: float = Field(default=0,ge=0,le=1)

@app.post("/v1/regression")
def compare(body: RegressionRequest):
    return regression(body.baseline,body.candidate,body.tolerance)
