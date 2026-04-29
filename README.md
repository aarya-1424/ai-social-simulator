# 🧠 AI Multi-Agent Social Simulation System

A full-stack AI system that simulates how different personas respond, reason, interact, and defend their opinions on a given topic.
This project demonstrates **multi-agent AI architecture**, **tool-based reasoning**, and **prompt-injection defense**, built using modern LLM workflows.

--------------------------------------------------------------------------------------------------------------

## ✨ Demo Overview

The system takes a user input (e.g., a social media post) and:

1. Routes it to relevant AI agents using semantic similarity
2. Each agent:
   - Thinks (chooses a perspective)
   - Uses context (mock retrieval)
   - Generates a response
3. Agents interact (debate-style replies)
4. System defends against malicious or misleading inputs

---------------------------------------------------------------------------------------------------------------

## 🧩 Features

- 🔀 **Embedding-based Routing**  
  Selects relevant agents using semantic similarity

- 🧠 **Multi-Agent System**  
  Each agent has a unique persona (optimist, skeptic, finance-driven, etc.)

- 🔎 **Tool-Augmented Reasoning**  
  Agents simulate context retrieval before generating responses

- 💬 **Agent Interaction**  
  Agents respond to each other, forming a debate

- 🛡️ **Prompt Injection Defense**  
  Prevents malicious inputs from altering agent behavior

- 🎨 **Modern UI (React + Tailwind)**  
  Clean black-themed dashboard visualizing the full pipeline

---------------------------------------------------------------------------------------------------------------

## 🏗️ Architecture
User Input
↓
Router (Embeddings)
↓
Relevant Agents
↓
Each Agent:
→ Think (LLM)
→ Retrieve Context (Tool)
→ Generate Response (LLM)
↓
Agent Interaction (Debate)
↓
Defense Layer (Prompt Injection Handling)
↓
Frontend UI


-----------------------------------------------------------------------------------------------------------------

## 🧠 Agents

| Agent        | Persona |
|-------------|--------|
| tech_max     | Optimistic AI enthusiast |
| doomer       | Pessimistic critic |
| finance_bro  | Profit-driven thinker |

-----------------------------------------------------------------------------------------------------------------

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- LangGraph (agent workflow)
- Groq API (LLM inference)
- Sentence Transformers (embeddings)

### Frontend
- React
- Tailwind CSS
- Framer Motion

-----------------------------------------------------------------------------------------------------------------

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/aarya-1424/ai-social-simulator.git
cd ai-social-simulator

2. Backend Setup
pip install -r requirements.txt

Create .env:
GROQ_API_KEY=your_api_key_here

Run server:
uvicorn api:app --reload

3. Frontend Setup
cd Frontend
npm install
npm run dev

-----------------------------------------------------------------------------------------------------------------

🚀 Future Improvements
Real-time streaming responses
Multi-turn conversation loops
Database for storing simulations
Advanced RAG with real search APIs
User authentication & session history

-----------------------------------------------------------------------------------------------------------------

🎯 Key Learnings
Designing multi-agent AI systems
Combining LLMs with tools (RAG concept)
Handling prompt injection attacks
Building full-stack AI applications

-----------------------------------------------------------------------------------------------------------------

👤 Author
Built by Aarya Kapoor

-----------------------------------------------------------------------------------------------------------------

⭐ If you like this project
Give it a star and feel free to fork!

-----------------------------------------------------------------------------------------------------------------
