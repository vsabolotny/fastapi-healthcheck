from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse, PlainTextResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.get("/health", response_class=PlainTextResponse)
def get_health_status():
    return "health status is green"

class AskRequest(BaseModel):
    query: str

@app.post("/askme", response_class=JSONResponse)
def ask_openai(request: AskRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[
                {"role": "user", "content": request.query}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))