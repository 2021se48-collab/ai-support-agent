from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from app.agent.agent_core import get_ai_response
import os

load_dotenv()

app = FastAPI(
    title="AI Support Agent",
    description="AI-powered customer support agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str
    session_id: str

@app.get("/")
def root():
    return {"status": "AI Support Agent is running!"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = get_ai_response(request.message, request.session_id)
    return ChatResponse(reply=reply, session_id=request.session_id)