from openai import AsyncOpenAI
from settings import OPENAI_API_KEY
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def openai_response(role: str, prompt: str):
    try:
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            timeout=25.0  # Increased timeout but still under Heroku's 30s limit
        )
        
        response = await client.chat.completions.create(
            model="gpt-4",  # Fixed model name
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        raise Exception(f"Error calling OpenAI API: {str(e)}")