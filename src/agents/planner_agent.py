"""
Planner Agent - Decompose problems into multi-step plans
"""

import json
import re
from typing import List, Dict
from utils.model_loader import ModelLoader
from utils.rag_retriever import RAGRetriever


class PlannerAgent:
    """Problem decomposition agent"""
    
    def __init__(self, adapter_path: str, rag_retriever: RAGRetriever, model_loader: ModelLoader):
        self.model_loader = model_loader
        self.model = self.model_loader.load_adapter(adapter_path, "planner")
        self.rag = rag_retriever
    
    def plan(self, problem: str) -> List[Dict]:
        """Generate execution plan for problem"""
        
        examples = self.rag.retrieve_decomposition_examples(problem, top_k=2)
        examples_text = "\n\n".join(examples)
        
        # --- START OF FIX ---
        # A single, raw f-string prompt.
        # We add "The plan is:" at the end to force it to start generating the plan.
        prompt = f"""You are a problem decomposition expert. Your task is to break down a problem into clear, executable steps.
Provide *ONLY* the steps, one per line. Do NOT include reasoning, explanations, or any text other than the steps themselves.

RELEVANT EXAMPLES:
{examples_text}

PROBLEM TO DECOMPOSE:
{problem}

The plan is:
"""
        
        self.model.set_adapter("planner")
        response = self.model_loader.generate(self.model, prompt, max_length=1024)
        
        # Better parsing
        plan_steps = []
        for line in response.split('\n'):
            step_text = re.sub(r"^\s*(\d+\.|-|\*|Step \d+:)\s*", "", line).strip()
            
            # Filter out junk lines
            if step_text and any(c.isalpha() for c in step_text) and "</think>" not in step_text:
                plan_steps.append({"step": step_text})
        # --- END OF FIX ---
        
        if not plan_steps:
             return [{"step": "Could not determine plan."}]
             
        return plan_steps
