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
# LLM Semantic Router (IMPROVED)
# -------------------------------
def route_post_to_bots(post):
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

    # -------------------------------
    # VALIDATION
    # -------------------------------
    valid_ids = [bot["bot_id"] for bot in personas]
    matched_bots = [bot_id for bot_id in matched_bots if bot_id in valid_ids]

    # -------------------------------
    # 🔥 FORCE ALL 3 AGENTS (SMART FIX)
    # -------------------------------
    if len(matched_bots) < 2:
        matched_bots = valid_ids[:2]

    # Add missing agents to make total = 3
    for bot_id in valid_ids:
        if bot_id not in matched_bots:
            matched_bots.append(bot_id)

    # Ensure only 3 max
    matched_bots = matched_bots[:3]

    print("Selected Bots:", matched_bots)

    return matched_bots