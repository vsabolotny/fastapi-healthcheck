from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse, PlainTextResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for LLM provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # Default to OpenAI

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Placeholder for other LLM clients (e.g., Anthropic)
# You can initialize other clients here as needed.

app = FastAPI()

@app.get("/health", response_class=PlainTextResponse)
def get_health_status():
    return "health status is green"

class AskRequest(BaseModel):
    query: str

def llm_factory(provider: str, query: str):
    """
    Factory function to handle different LLM providers.
    """
    if provider == "openai":
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content.strip()
    elif provider == "anthropic":
        # Example for Anthropic (replace with actual implementation)
        # response = anthropic_client.some_method(query)
        return "Anthropic response placeholder"
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

@app.post("/askme", response_class=JSONResponse)
def ask_openai(request: AskRequest):
    try:
        answer = llm_factory(LLM_PROVIDER, request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))