title: Customer Support AI Environment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: inference.py
pinned: false
📧 Customer Support AI Environment (OpenEnv)
🚀 Overview
This project implements a real-world customer support simulation environment using the OpenEnv specification. It allows AI agents (LLMs) to interact with customer queries and be evaluated based on the quality of their responses.

The environment is designed to model how real customer support systems work, including:

Understanding customer queries
Generating appropriate responses
Handling multi-step issues
Deciding when escalation is needed
🎯 Motivation
Customer support is a high-impact real-world application of AI. This environment provides a structured way to:

Evaluate LLM performance on support tasks
Benchmark reasoning and response quality
Train agents for real-world deployment
It fills a gap by offering a lightweight, deterministic, and reproducible evaluation setup for conversational agents.

🧠 Environment Design
🔍 Observation Space
Each step provides:

message_id (int): Unique identifier
customer_message (string): User query
conversation_history (list): Previous messages
⚡ Action Space
Agent outputs:

response_message (string): Reply to customer
escalate_to_human (bool): Optional escalation
🏆 Reward Function
Reward ∈ [0.0, 1.0]

Based on keyword overlap with expected answer
Partial credit for partially correct responses
Penalty for unnecessary escalation
This ensures:

Dense reward signal (not just binary)
Encourages meaningful progress
🔄 Environment Methods
reset() → returns initial observation
step(action) → returns (observation, reward, done, info)
state() → returns current environment state
📚 Tasks (Easy → Hard)
🟢 Easy
Simple FAQ (e.g., working hours)
Requires direct factual response
🟡 Medium
Multi-step query (e.g., password reset)
Requires understanding + instruction
🔴 Hard
Real-world issue (e.g., wrong product received)
Requires reasoning + next-step guidance
🧪 Grader Design
Deterministic keyword-based scoring
Produces scores between 0.0 and 1.0
Fully reproducible across runs
🤖 Baseline Inference
File: inference.py

Uses OpenAI client (optional)
Default mode: deterministic mock responses (for reproducibility)
Produces structured logs:
[START]
[STEP] ...
[END]
⚠️ Note
Due to API quota limits, the baseline runs in mock mode by default. However, OpenAI integration is supported via:

OPENAI_API_KEY
MODEL_NAME
API_BASE_URL
📦 Installation & Setup
1. Install dependencies
pip install -r requirements.txt
2. Run environment
python env.py
3. Run baseline inference
python inference.py
🐳 Docker Usage
Build image
docker build -t customer_support_env .
Run container
docker run customer_support_env
(Optional: pass API key)

docker run --env OPENAI_API_KEY="your_key" customer_support_env
📊 Baseline Results
Task	Score
Easy	1.0
Medium	1.0
Hard	1.0
Total	3.0
✅ OpenEnv Compliance
✔ Typed Observation, Action, Reward models (Pydantic)
✔ step(), reset(), state() implemented
✔ openenv.yaml included
✔ Deterministic graders
✔ 3 tasks with increasing difficulty
💡 Creativity & Novelty
Simulates customer support workflows

Includes reward shaping for conversational quality

Supports both:

Deterministic evaluation
Real LLM interaction
🚀 Future Improvements
Multi-turn conversations
Sentiment-aware responses
Advanced grading using semantic similarity
Integration with real support datasets
👩‍💻 Author
Aditi Sinha 
Ekansh Amar

📜 License
MIT