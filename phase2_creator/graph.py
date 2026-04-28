import os
from typing import TypedDict, List

from dotenv import load_dotenv
from groq import Groq
from langgraph.graph import StateGraph, END

# ---------------------------------
# Load environment variables
# ---------------------------------
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------------
# Optional tool fallback
# ---------------------------------
try:
    from phase2_creator.tools import mock_search
except ImportError:
    def mock_search(topic: str):
        return f"No external tool found. Basic context for: {topic}"


# ---------------------------------
# Graph State
# ---------------------------------
class GraphState(TypedDict, total=False):
    input_post: str
    persona: str
    selected_bots: List[str]
    responses: List[str]
    topic: str
    context: str
    final_post: str


# ---------------------------------
# STEP 1: Decide topic
# ---------------------------------
def decide_topic(state: GraphState):
    post = state.get("input_post", "")
    persona = state.get("persona", "You are a helpful AI assistant.")

    prompt = f"""
You are this persona:
{persona}

Given this post:
{post}

Choose the most interesting angle/topic to respond to.
Reply in one short line only.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )

    topic = response.choices[0].message.content.strip()

    return {"topic": topic}


# ---------------------------------
# STEP 2: Search context
# ---------------------------------
def search_context(state: GraphState):
    topic = state.get("topic", "")
    context = mock_search(topic)
    return {"context": context}


# ---------------------------------
# STEP 3: Generate final response
# ---------------------------------
def generate_response(state: GraphState):
    persona = state["persona"]
    topic = state["topic"]
    context = state["context"]

    prompt = f"""
You are this persona:
{persona}

Topic:
{topic}

Context:
{context}

Write a strong, opinionated social media post (5-6 lines).
Use the context to support your argument.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    final_post = response.choices[0].message.content.strip()

    return {"final_post": final_post}


# ---------------------------------
# Build Graph
# ---------------------------------
builder = StateGraph(GraphState)

builder.add_node("decide_topic", decide_topic)
builder.add_node("search", search_context)
builder.add_node("generate", generate_response)

builder.set_entry_point("decide_topic")

builder.add_edge("decide_topic", "search")
builder.add_edge("search", "generate")
builder.add_edge("generate", END)

graph = builder.compile()