import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def reply_to_agent(persona, other_response, original_post):
    prompt = f"""
    You are this persona:
    {persona}

    Original post:
    {original_post}

    Another agent said:
    {other_response}

    Your task:
    - Respond to that agent
    - Agree or disagree strongly
    - Stay in your personality
    - Add new perspective

    Write 4-6 lines.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()