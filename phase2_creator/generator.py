import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_post(persona, topic):
    prompt = f"""
    You are this persona:
    {persona}

    Topic: {topic}

    Write a strong, opinionated post (5-7 lines).
    Explain your reasoning clearly.
    Make it engaging and slightly argumentative.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content