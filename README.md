# SaptangAgent-v2 — Multi-Agent Procedural Reasoning System
Hackathon Project – Saptang Labs Machine Learning Challenge

Project Overview

SaptangAgent-v2 is an AI-powered multi-agent system capable of solving logical and mathematical reasoning problems.
It works using coordinated agents that break down problems into smaller steps, execute solutions using external tools, verify correctness, and refine the final answers.

System Architecture — Multi-Agent Workflow
Agent	Role
-Planner Agent	Decomposes complex problems into step-by-step plans
-Executor Agent	Executes each step using tools like SymPy, PuLP, Z3, Calculator
-Validator Agent	Verifies if execution results follow the correct logic
-Refiner Agent	Improves final answer if the Validator demands refinements
-Meta-Decider	Routes and controls agent interaction

Tools Used:-
-SymPy Solver
-PuLP Optimizer
-Z3 Constraint Solver
-Math Calculator
-RAG-based Query System
-LoRA-based adapters for role-specific intelligence

Project Structure
SaptangAgent-v2/
│
├── models/           # LORA adapters (Planner, Executor, Refiner)
├── tools/            # Calculator, SymPy, PuLP, Z3 integrations
├── core/             # Main agent & orchestration logic
├── data/
│   ├── train_math.csv
│   └── train_procedural.csv
├── logs/             # Execution logs (traces & reasoning history)
├── main.ipynb        # Execution pipeline notebook
└── README.md         # You're reading it :)

Results
Dataset	Accuracy	Avg Pipeline Time
Math Reasoning	~61.5%	80–120 sec/problem
System performs strongly on well-structured reasoning and arithmetic logic tasks.

Team Contributions
Member	Responsibility
Member 1 – Planner + Decomposer	Designing problem-decomposition logic, planning system, and plan-trace logging
Member 2 – Execution + Tools Integration	Connecting solvers (SymPy, PuLP, Z3), execution loop, and tool routing
Member 3 – Refinement + Validation	Final answer improvement loop, dual-verification cycle, failure recovery
Member 4 – Future Deployment (Upcoming)	Cloud deployment: Docker, API, Streamlit UI / Web interface

Note: Deployment will be added in the future update once backend APIs are fully stable.

🧪 How to Run
git clone https://github.com/Subodhkhanduri/Ethos_ML_Challenge/tree/main
cd Ethos_ML_Challenge
pip install -r requirements.txt
python main.py
Or run the main.ipynb file directly in Colab for GPU support.

Future Scope
✔ Scale to 7B–13B parameter LLM
✔ Reflexive double-verification for reduced reasoning errors
✔ Memory optimization for long-loop reasoning
✔ Dynamic tool creation at runtime
✔ Web deployment with optimized model serving (by Member-4)

Note:-
We are still improving the system’s stability & accuracy.
Suggestions and feedback are welcome! 😊

Acknowledgment:-
Thanks to Saptang Labs for providing the challenge, datasets, and support.
