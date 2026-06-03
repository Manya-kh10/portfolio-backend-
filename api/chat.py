from fastapi import APIRouter, HTTPException
from api.models import ChatRequest, ChatResponse
from api.agent.chat import ask_agent

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_twin(request: ChatRequest):
    """
    POST route allowing website visitors to converse with Manya's Digital Twin AI agent.
    """
    # Guard against empty messages
    if not request.message or not request.message.strip():
        return ChatResponse(response="Hey! Go ahead and ask me anything about Manya.")

    try:
        reply = ask_agent(request.message)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Digital Twin Agent error: {str(e)}")