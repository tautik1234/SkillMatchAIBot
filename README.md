# 🧠 SkillMatch AI Bot

> **Next-Generation AI Career Mentor & Contextual Skill-Gap Conversational Agent**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-green?logo=node.js&logoColor=white)](https://nodejs.org/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![LLM](https://img.shields.io/badge/LLM-Groq%20LLaMA--3.3--70B-f55036?logo=groq&logoColor=white)](https://groq.com/)
[![Architecture](https://img.shields.io/badge/Architecture-3--Tier%20BFF%20Microservices-blueviolet)](#-system-architecture)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

**SkillMatch AI Bot** is an intelligent, low-latency conversational agent designed to bridge the chasm between candidates' current skills and industry job requirements. 

Unlike generic chatbots, SkillMatch AI Bot operates in **two specialized modes**:
1. **Global Career Mentor**: Provides comprehensive career guidance, structured learning roadmaps, placement advice, and mock interview preparations.
2. **Context-Aware Skill-Gap Remediation**: Ingests missing skills and target roles directly from candidate profiles, automatically tailoring custom roadmaps, project recommendations, and interview questions to close specific competency deficits.

The system is built upon a **decoupled, polyglot 3-tier microservice architecture** using **React 19**, a **Node.js Express Backend-For-Frontend (BFF)** proxy, and a high-performance **Python Flask AI service** powered by **Groq Cloud's LLaMA 3.3 70B Versatile** engine.

---

## ✨ Key Features

- 🎯 **Dual-Mode Conversational Engine**:
  - `global` Mode: Serves as a 24/7 career counselor, advising on career trajectories, technology stacks, certifications, and portfolio building.
  - `skill_gap` Mode: Dynamically primes the system prompt with candidate-specific metadata (`target_role` and `missing_skill`) for laser-targeted upskilling roadmaps.
- ⚡ **Ultra-Low Latency Inference**: Utilizes Groq LPUs with the `llama-3.3-70b-versatile` model for lightning-fast token generation and near-instantaneous replies.
- 🛡️ **Strict Domain Guardrails**: Hardened system prompts prevent prompt injection, hallucinations, and out-of-domain conversations, maintaining a consistent professional mentorship persona.
- 💡 **Interactive Suggestion Chips**: Context-aware prompts help users quickly discover relevant learning paths, projects, and interview questions with one click.
- 🧩 **Clean Microservice Separation**: Prevents vendor lock-in and isolates frontend traffic from the AI execution layer via an Express API Gateway.
- 💻 **Streaming CLI Harness**: Includes a standalone Python script (`test.py`) for command-line testing with live token streaming.

---

## 🏗️ System Architecture

```
                                  +---------------------------------------+
                                  |             CLIENT LAYER              |
                                  |                                       |
                                  |     React 19 SPA (Vite) [:5173]       |
                                  |     Component: frontend/src/Chat.jsx  |
                                  +---------------------------------------+
                                                      |
                                                      | HTTP POST /api/chat
                                                      | Payload: { messages, mode, skill, role }
                                                      v
                                  +---------------------------------------+
                                  |          EDGE GATEWAY / BFF           |
                                  |                                       |
                                  |     Node.js + Express [:5000]         |
                                  |     backend/app.js                    |
                                  |     backend/routes/chat.js            |
                                  +---------------------------------------+
                                                      |
                                                      | HTTP POST /chat (Reverse Proxy)
                                                      | Payload: { messages, mode, skill, role }
                                                      v
                                  +---------------------------------------+
                                  |            AI MICROSERVICE            |
                                  |                                       |
                                  |     Python 3.10+ Flask [:5001]        |
                                  |     agent_api.py                      |
                                  +---------------------------------------+
                                                      |
                                                      | HTTPS SDK Calls
                                                      | System Prompt + Guardrails
                                                      v
                                  +---------------------------------------+
                                  |            GROQ CLOUD LPU             |
                                  |                                       |
                                  |     Model: llama-3.3-70b-versatile    |
                                  +---------------------------------------+
```

---

## 📂 Repository Structure

```text
SkillMatchAIBot/
├── .env.example                                  # Template for environment variables
├── .gitignore                                    # Git ignore rules (node_modules, venv, .env)
├── README.md                                     # Project documentation
├── agent_api.py                                  # Flask AI Microservice (Groq LLaMA 3.3)
├── requirements.txt                              # Python package dependencies
├── test.py                                       # CLI streaming test script for Groq
│
├── backend/                                      # Node.js BFF / API Gateway
│   ├── app.js                                    # Express application entry point (Port 5000)
│   ├── package.json                              # Node dependencies (express, cors, axios)
│   └── routes/
│       └── chat.js                               # /api/chat route proxying requests to Flask
│
└── frontend/                                     # React 19 Client SPA
    ├── index.html                                # HTML entry point
    ├── package.json                              # Frontend dependencies (React 19, Vite 6)
    ├── vite.config.js                            # Vite bundler configuration
    ├── public/                                   # Static assets (favicons, icons)
    └── src/
        ├── App.jsx                               # Root application component
        ├── App.css                               # Root application styles
        ├── Chat.jsx                              # Core Chat UI & state management
        ├── Chat.css                              # Glassmorphic, dark-mode chat styling
        ├── index.css                             # Global typography & layout rules
        └── main.jsx                              # React DOM mounting
```

---

## 🔌 API Reference

### 1. BFF Gateway Endpoint
`POST http://localhost:5000/api/chat`

The React frontend sends user conversations to the Express Gateway, which validates and forwards them to the Python AI service.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Payload (Global Mode)
```json
{
  "mode": "global",
  "messages": [
    {
      "role": "user",
      "content": "How do I build a roadmap to become a Backend Developer?"
    }
  ]
}
```

#### Request Payload (Skill-Gap Mode)
```json
{
  "mode": "skill_gap",
  "skill": "Docker",
  "role": "Backend Engineer",
  "messages": [
    {
      "role": "user",
      "content": "Docker Roadmap"
    }
  ]
}
```

#### Response Format
```json
{
  "reply": "### 🚀 4-Week Docker Mastery Roadmap for Backend Engineers\n\n1. **Week 1: Fundamentals**\n   - Containers vs. Virtual Machines\n   - Core Docker CLI commands (`docker run`, `docker ps`, `docker exec`)\n..."
}
```

---

### 2. Python AI Microservice Endpoint
`POST http://localhost:5001/chat`

Handles system prompt assembly, role/skill injection, and Groq API completions.

---

## 🚀 Quick Start Guide

### Prerequisites

Ensure you have the following installed on your machine:
- **Python**: Version `3.10` or higher
- **Node.js**: Version `18.0.0` or higher (with `npm`)
- **Groq API Key**: Obtain a free API key from [Groq Console](https://console.groq.com/)

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/tautik1234/SkillMatchAIBot.git
cd SkillMatchAIBot
```

---

### Step 2: Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

---

### Step 3: Run the Python AI Microservice

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start the Flask service (runs on http://127.0.0.1:5001)
python agent_api.py
```

---

### Step 4: Run the Express API Gateway

In a new terminal window:

```bash
cd backend

# Install Node dependencies
npm install

# Start the Express server (runs on http://localhost:5000)
node app.js
```

---

### Step 5: Run the React Frontend

In a third terminal window:

```bash
cd frontend

# Install frontend dependencies
npm install

# Launch Vite development server
npm run dev
```

Open your browser and navigate to **`http://localhost:5173`**.

---

### Step 6: (Optional) Test via CLI

If you want to test the Groq LLM agent with live streaming in your terminal without launching the frontend or backend servers:

```bash
python test.py
```

---

## 🎯 Dual-Mode Usage Examples

| Feature | `mode: "global"` | `mode: "skill_gap"` |
| :--- | :--- | :--- |
| **Trigger** | Default landing state | Launched with `skill` and `role` props |
| **Initial Prompt** | Overview of capabilities (Roadmaps, Certs, Interviews) | Mentions the exact missing skill and target role |
| **Banner Display** | Standard Header | Prominent badges showing **Missing Skill** & **Target Role** |
| **Prompt Injection** | Standard career mentorship rules | Injects target role, missing skill, and prioritized learning roadmap instructions |
| **Default Chips** | `"Backend Developer roadmap"`, `"How do I learn React?"` | `"<Skill> Roadmap"`, `"<Skill> Projects"`, `"<Skill> Certifications"` |

---

## 💡 Core Design Decisions & Engineering Highlights

- **BFF (Backend-For-Frontend) Pattern**: Express acts as an edge proxy isolating client requests from internal microservice APIs and LLM secrets.
- **Polyglot Microservices**: Combines Node.js (high-concurrency routing and lightweight proxying) with Python (native ecosystem for AI/ML inference).
- **Stateless Agent Design**: The Python Flask service maintains zero conversational state in memory; conversation history is passed through authenticated payloads, ensuring horizontal scalability.
- **Prompt Hardening**: Strict boundary conditions protect against jailbreaks, off-topic hallucinations, and unnecessary token burn.

---

## 🛡️ Security & Guardrails

- **Environment Isolation**: API keys (`GROQ_API_KEY`) are kept strictly on the backend/microservice level and are never exposed to the client.
- **System Prompt Boundaries**: The AI model is strictly instructed to decline unrelated queries (e.g., general trivia, math, entertainment) with a polite refusal message to conserve tokens and maintain platform focus.
- **CORS Protection**: Both the Express Gateway and Flask microservice implement Cross-Origin Resource Sharing controls.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <sub>Built with ❤️ for aspiring engineers and recruiters by <a href="https://github.com/tautik1234">tautik1234</a>.</sub>
</div>
