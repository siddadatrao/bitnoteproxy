from openai import OpenAI
from settings import OPENAI_API_KEY
import asyncio

async def openai_response(role: str, prompt: str):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY, timeout=25.0)  # Set timeout to 25 seconds
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,  # Limit response length
            timeout=25  # Set OpenAI timeout
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        raise Exception(f"Error calling OpenAI API: {str(e)}")