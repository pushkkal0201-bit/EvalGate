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
