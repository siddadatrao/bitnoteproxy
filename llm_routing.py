from openai import AsyncOpenAI
from settings import OPENAI_API_KEY

async def openai_response(role: str, prompt: str):
    try:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        response = await client.chat.completions.create(
            model="gpt-4o",  # Using a faster model
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            timeout=20
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        raise Exception(f"Error calling OpenAI API: {str(e)}")