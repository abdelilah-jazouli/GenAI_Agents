from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from agent import ConversationalAgent
from prompts import PREDEFINED_PROMPTS
import json
import uvicorn

app = FastAPI(title="Conversational Agent API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser l'agent
agent = ConversationalAgent(db_path="conversations.db")

# Modèles Pydantic pour la validation des données
class Message(BaseModel):
    content: str
    session_id: str = "default_user"

class SystemPrompt(BaseModel):
    prompt: str
    session_id: str

class Session(BaseModel):
    session_id: str
    system_prompt: str
    last_updated: str

class ChatHistory(BaseModel):
    messages: List[dict]

@app.get("/")
async def get_home():
    """Retourne la page HTML principale"""
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

@app.post("/chat")
async def chat(message: Message):
    """Endpoint pour envoyer un message et recevoir une réponse"""
    try:
        response = agent.chat(message.content, message.session_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
async def list_sessions():
    """Liste toutes les sessions disponibles"""
    sessions = agent.list_sessions()
    return [
        {
            "session_id": session_id,
            "system_prompt": prompt,
            "last_updated": last_updated
        }
        for session_id, prompt, last_updated in sessions
    ]

@app.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Récupère l'historique d'une session"""
    history = agent.get_conversation_history(session_id)
    return {"messages": [{"role": role, "content": content} for role, content in history]}

@app.post("/sessions/{session_id}/prompt")
async def set_system_prompt(session_id: str, prompt_data: SystemPrompt):
    """Définit le prompt système pour une session"""
    agent.set_system_prompt(prompt_data.prompt, session_id)
    return {"status": "success"}

@app.delete("/sessions/{session_id}")
async def reset_session(session_id: str):
    """Réinitialise une session"""
    agent.reset_conversation(session_id)
    return {"status": "success"}

# WebSocket pour le chat en temps réel
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            response = agent.chat(message, session_id)
            await websocket.send_text(json.dumps({
                "response": response,
                "session_id": session_id
            }))
    except Exception as e:
        await websocket.close()

# Ajouter ces endpoints à web_app.py

@app.get("/prompts")
async def list_prompts():
    """Retourne la liste des prompts prédéfinis"""
    return PREDEFINED_PROMPTS

@app.get("/sessions/{session_id}/prompt")
async def get_system_prompt(session_id: str):
    """Récupère le prompt système actuel d'une session"""
    prompt = agent._get_system_prompt(session_id)
    return {"prompt": prompt}

@app.post("/sessions/{session_id}/use_prompt/{prompt_type}")
async def use_predefined_prompt(session_id: str, prompt_type: str):
    """Utilise un prompt prédéfini pour une session"""
    if prompt_type not in PREDEFINED_PROMPTS:
        raise HTTPException(status_code=404, detail="Prompt type not found")
    agent.set_system_prompt(PREDEFINED_PROMPTS[prompt_type], session_id)
    return {"status": "success"}

@app.get("/sessions/{session_id}/full_history")
async def get_full_session_history(session_id: str):
    """Récupère l'historique complet d'une session avec les métadonnées"""
    history = agent.get_conversation_history(session_id)
    prompt = agent._get_system_prompt(session_id)
    return {
        "session_id": session_id,
        "system_prompt": prompt,
        "messages": [{"role": role, "content": content} for role, content in history]
    }

if __name__ == "__main__":
    uvicorn.run("web_app:app", host="0.0.0.0", port=8000, reload=True)
