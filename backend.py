from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from llm_routing import openai_response
from settings import llm_type

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
            response_text = openai_response(role, prompt)
            return {"response": response_text}
        raise HTTPException(status_code=400, detail="Invalid LLM type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
