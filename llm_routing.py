from openai import OpenAI
from settings import OPENAI_API_KEY

def openai_response(prompt, role="You are a helpful assistant"):

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content