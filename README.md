# **SaptangAgent-v2**  
### *A Multi-Agent Procedural Reasoning System*  
**Hackathon Project – Saptang Labs Machine Learning Challenge**

---

## **1. Project Overview**
SaptangAgent-v2 is a modular, AI-powered multi-agent system designed to solve logical, mathematical, and procedural reasoning problems. The system operates through coordinated specialized agents that decompose complex problems, execute solutions using external tools, validate correctness, and refine results to ensure high-quality outputs.

---

## **2. System Architecture**
SaptangAgent-v2 follows a structured multi-agent workflow with clearly defined roles:

| **Agent**        | **Role Description** |
|------------------|----------------------|
| **Planner Agent** | Decomposes complex problems into step-by-step executable plans |
| **Executor Agent** | Executes individual steps using computational tools |
| **Validator Agent** | Verifies logical consistency and correctness of outputs |
| **Refiner Agent** | Improves outputs based on validator feedback |
| **Meta-Decider** | Controls routing, sequencing, and coordination among agents |

---

## **3. Integrated Tools**
The system leverages multiple external reasoning and optimization tools:
- **SymPy Solver**
- **PuLP Optimizer**
- **Z3 Constraint Solver**
- **Mathematical Calculator**
- **RAG-based Query System**
- **LoRA-based Adapters** for role-specific intelligence

---

## **4. Project Structure**
SaptangAgent-v2/
│
├── models/           # LoRA adapters (Planner, Executor, Refiner)
├── tools/            # Calculator, SymPy, PuLP, Z3 integrations
├── core/             # Main agent orchestration logic
├── data/
│   ├── train_math.csv
│   └── train_procedural.csv
├── logs/             # Execution logs (traces & reasoning history)
├── main.ipynb        # Execution pipeline notebook
└── README.md         # You're reading it :)

## **5. Performance & Results**

| **Dataset**    | **Accuracy** | **Avg. Pipeline Time** |
| -------------- | ------------ | ---------------------- |
| Math Reasoning | ~61.5%       | 80–120 sec/problem     |
The system demonstrates strong performance on well-structured mathematical and procedural reasoning tasks.


## **6. Team Contributions**

| **Team Member**     | **Responsibility**                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| **Kaushiki Singh**  | Planner & Decomposer: Designed problem decomposition logic, planning system, and trace logging |
| **Subodh Khanduri** | Execution & Tool Integration: Integrated SymPy, PuLP, Z3, and built execution loop             |
| **Kaukab Erum**     | Validation & Refinement: Dual-verification cycles, output refinement, failure recovery         |
| **Komal Kumari**    | Future Deployment (Upcoming): Dockerization, API backend, Streamlit Web UI                     |

Note: Deployment will be added in the future update once backend APIs are fully stable.

## **7. Installation & Execution**

Step 1: Clone the Repository
git clone https://github.com/Subodhkhanduri/Ethos_ML_Challenge/tree/main

Step 2: Navigate to the Project Directory
cd Ethos_ML_Challenge

Step 3: Install Dependencies
-pip install -r requirements.txt

Step 4: Run the System
-python main.py
-Or run the main.ipynb file directly in Colab for GPU support.

## **8. Future Scope**
✔ Scale to 7B–13B parameter LLM
✔ Reflexive double-verification for reduced reasoning errors
✔ Memory optimization for long-loop reasoning
✔ Dynamic tool creation at runtime
✔ Web deployment with optimized model serving (by Member-4)

Note:-
We are still improving the system’s stability & accuracy.
Suggestions and feedback are welcome! 

## **Acknowledgment:-**
Thanks to Saptang Labs for providing the challenge, datasets, and support.
