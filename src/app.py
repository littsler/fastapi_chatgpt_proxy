import logging
import os
from typing import Dict, List
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai


class ChatRequest(BaseModel):
    model: str
    temperature: float = 1.0
    stop: str = None
    api_key: str = None
    messages: List[Dict[str, str]]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="")
# app.mount("/static", StaticFiles(directory="static/static"), name="static")

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.get("/")
async def root():
    # Return the contents of the 'index.html' file
    with open("static/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/chat")
def read_root(chat_request: ChatRequest):
    if chat_request.api_key:
        openai.api_key = chat_request.api_key
    logging.info(str(chat_request))
    response = openai.ChatCompletion.create(
        model=chat_request.model,
        temperature=chat_request.temperature,
        stop=chat_request.stop,
        messages=chat_request.messages
    )
    reply = response["choices"][0]["message"]["content"]
    openai.api_key = os.getenv('OPENAI_API_KEY')
    logging.info(f"Reply: {reply}")
    return {"sender": "bot", "text": reply}

@app.get("/isAlive")
def is_alive():
    return {"is_alive": True}
