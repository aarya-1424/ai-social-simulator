import os
import json
from dotenv import load_dotenv
from groq import Groq

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------
# Load personas
# -------------------------------
with open("data/personas.json", "r", encoding="utf-8") as file:
    personas = json.load(file)


# -------------------------------
# LLM Semantic Router
# -------------------------------
def route_post_to_bots(post, threshold=0.4):
    """
    threshold kept only for compatibility with old code.
    Not used anymore.
    """

    bot_list = "\n".join(
        [f"{bot['bot_id']}: {bot['persona']}" for bot in personas]
    )

    prompt = f"""
You are an intelligent routing system for a social media simulator.

User Post:
{post}

Available Bots:
{bot_list}

Task:
Choose the 2 most relevant bots who should respond to this post.

Rules:
- Pick bots based on topic, tone, emotion, controversy, and relevance.
- Return ONLY bot_ids separated by commas.
- No explanation.

Example:
tech_max,doomer
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    text = response.choices[0].message.content.strip()

    matched_bots = [x.strip() for x in text.split(",") if x.strip()]

    # safety fallback
    valid_ids = [bot["bot_id"] for bot in personas]
    matched_bots = [bot_id for bot_id in matched_bots if bot_id in valid_ids]

    # fallback if model gives bad output
    if len(matched_bots) == 0:
        matched_bots = [personas[0]["bot_id"]]

    print("Selected Bots:", matched_bots)

    return matched_bots