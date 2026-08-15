from fastapi import FastAPI
from pydantic import BaseModel

from agents.orchestrator import OrchestratorAgent


app = FastAPI(
    title="BPM Agentic AI Assistant"
)


agent = OrchestratorAgent()



class BPMRequest(BaseModel):

    query: str



@app.get("/")
def home():

    return {
        "message": "BPM Agentic AI is running"
    }



@app.post("/analyze")
def analyze_process(
        request: BPMRequest
):

    result = agent.execute(
        request.query
    )

    return {
        "response": result
    }