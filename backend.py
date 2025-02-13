from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from llm_routing import openai_response
from settings import llm_type
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/response_router")
async def response_router(role: str, prompt: str):
    try:
        if llm_type == "openai":
            # Create a task with timeout
            response_text = await asyncio.wait_for(
                openai_response(role, prompt),
                timeout=30.0
            )
            return {"response": response_text}
        raise HTTPException(status_code=400, detail="Invalid LLM type")
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

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=30
    )
