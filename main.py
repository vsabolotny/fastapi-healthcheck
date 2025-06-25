# main.py
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/health", response_class=PlainTextResponse)
def get_health_status():
    return "health status is green"