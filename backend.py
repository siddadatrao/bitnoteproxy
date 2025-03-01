from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from llm_routing import openai_response
from settings import llm_type
import asyncio
from typing import Optional

app = FastAPI(
    title="BitNote API",
    description="API for handling AI responses and note-taking functionality",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    role: str = Field(
        description="The role/context for the AI response",
        example="You are a helpful ai that assists with programming tasks"
    )
    prompt: str = Field(
        description="The prompt/question to be processed",
        example="How do I implement a binary search tree in Python?"
    )
    conversation_history: Optional[list] = Field(
        default=None,
        description="Previous conversation messages for context"
    )

class PromptResponse(BaseModel):
    response: str = Field(
        description="The AI-generated response"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if something went wrong"
    )

@app.post(
    "/response_router",
    response_model=PromptResponse,
    description="Process a prompt and return an AI-generated response",
    responses={
        200: {"description": "Successful response"},
        422: {"description": "Invalid request format"},
        504: {"description": "Request timeout"},
        500: {"description": "Server error"}
    }
)
async def response_router(request: PromptRequest) -> PromptResponse:
    try:
        if llm_type != "openai":
            raise HTTPException(
                status_code=400,
                detail="Invalid LLM type configuration"
            )

        # Create a task with timeout
        response_text = await asyncio.wait_for(
            openai_response(request.role, request.prompt),
            timeout=30.0
        )
        
        return PromptResponse(response=response_text)

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Request timed out - please try again with a shorter prompt"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=30,
        log_level="info"
    )