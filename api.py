from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import json
import os

from phase1_router.router import route_post_to_bots
from phase2_creator.graph import graph
from phase3_defense.defense import generate_defense_reply

# --------------------------------------------------
# Create FastAPI App
# --------------------------------------------------
app = FastAPI()

# --------------------------------------------------
# Enable CORS (VERY IMPORTANT)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Load Personas
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
persona_path = os.path.join(BASE_DIR, "data", "personas.json")

with open(persona_path, "r", encoding="utf-8") as file:
    personas = json.load(file)

# --------------------------------------------------
# Request Model
# --------------------------------------------------
class InputData(BaseModel):
    post: str

# --------------------------------------------------
# Health Check Route
# --------------------------------------------------
@app.get("/")
def home():
    return {"message": "AI Social Simulator Backend Running"}

# --------------------------------------------------
# Main Simulation Route
# --------------------------------------------------
@app.post("/run-simulation")
def run_simulation(data: InputData):
    post = data.post

    matched_bots = route_post_to_bots(post)

    results = []

    for bot in personas:
        if bot["bot_id"] in matched_bots:

            result = graph.invoke({
                "input_post": post,
                "persona": bot["persona"]
            })

            results.append({
                "id": bot["bot_id"],
                "persona": bot["persona"],
                "topic": result.get("topic", ""),
                "context": result.get("context", ""),
                "final_post": result.get("final_post", "")
            })

    return {"agents": results}

# --------------------------------------------------
# Defense Route (Optional)
# --------------------------------------------------
@app.post("/defense")
def defense_reply(data: InputData):
    reply = generate_defense_reply(
        persona=personas[0]["persona"],
        conversation_history="User discussion ongoing.",
        user_input=data.post
    )

    return {"response": reply}