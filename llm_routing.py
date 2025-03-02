from openai import AsyncOpenAI
from settings import OPENAI_API_KEY
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fastapi import HTTPException
import asyncio
import json

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=6),
    retry=retry_if_exception_type((asyncio.TimeoutError, Exception)),
    reraise=True
)
async def openai_response(role: str, prompt: str):
    try:
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            timeout=25.0
        )
        
        # Use streaming to avoid timeouts
        stream = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            stream=True,
            temperature=0.7
        )

        # Accumulate the streamed response
        full_response = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content

        if not full_response:
            raise HTTPException(
                status_code=500,
                detail="Empty response from OpenAI"
            )

        return full_response

    except asyncio.TimeoutError as e:
        print(f"Timeout error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable due to timeout"
        )
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Service temporarily unavailable: {str(e)}"
        )