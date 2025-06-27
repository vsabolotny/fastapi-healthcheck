from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse, PlainTextResponse
import os
from dotenv import load_dotenv
from llm_strategy import LLMStrategyFactory  # Import the strategy logic

load_dotenv()

# Configuration for LLM provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # Default to OpenAI

app = FastAPI()

@app.get("/health", response_class=PlainTextResponse)
def get_health_status():
    return "health status is green"

class AskRequest(BaseModel):
    query: str

@app.post("/askme", response_class=JSONResponse)
def ask_openai(request: AskRequest):
    try:
        print(f"Using LLM provider: {LLM_PROVIDER}")
        strategy = LLMStrategyFactory.get_strategy(LLM_PROVIDER)
        answer = strategy.get_response(request.query)
        return {"answer": answer}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))