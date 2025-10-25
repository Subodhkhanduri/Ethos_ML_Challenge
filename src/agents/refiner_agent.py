"""
Refiner Agent - Convert technical traces to clean, human-readable solutions
"""

from typing import List, Dict, Any
from utils.model_loader import ModelLoader


class RefinerAgent:
    """Refines execution traces into clean, readable solutions"""
    
    def __init__(self, adapter_path: str, model_loader: ModelLoader):
        self.model_loader = model_loader
        self.model = self.model_loader.load_adapter(adapter_path, "refiner")
    
    def _format_trace(self, execution_trace: List[Dict[str, Any]]) -> str:
        formatted_trace = []
        for i, step in enumerate(execution_trace):
            trace_line = f"Step {i+1}:\n"
            trace_line += f"  - Task: {step.get('task', 'N/A')}\n" # Add task for context
            trace_line += f"  - Tool: {step.get('tool_used')}\n"
            trace_line += f"  - Input: {step.get('input')}\n"
            trace_line += f"  - Output: {step.get('output')}\n"
            trace_line += f"  - Result: {step.get('result')}\n"
            formatted_trace.append(trace_line)
        return "\n".join(formatted_trace)

    def refine(self, problem: str, execution_trace: List[Dict[str, Any]]) -> str:
        """
        Convert execution trace to clean solution
        """
        try:
            trace_text = self._format_trace(execution_trace)
            
            # --- START OF FIX ---
            # A single, raw f-string prompt.
            prompt = f"""You are a solution refiner. Convert the technical execution trace into a clean, human-readable solution.
Do not include technical jargon or tool names. Explain the steps clearly and provide the final answer.
Provide *ONLY* the final, refined solution, not your thoughts or self-reflection.

ORIGINAL PROBLEM:
{problem}

EXECUTION TRACE:
{trace_text}

Here is the clear, human-readable solution:
"""

            self.model.set_adapter("refiner")
            response = self.model_loader.generate(self.model, prompt, max_length=1024)
            return response
            # --- END OF FIX ---
            
        except Exception as e:
            print(f"Error in refiner: {e}")
            return "Could not refine solution."
