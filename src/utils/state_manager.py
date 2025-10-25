"""
State Manager - Manage agent memory and execution state
"""

from typing import List, Dict, Any


class StateManager:
    """Manage execution state and memory buffer"""
    
    def __init__(self, max_memory_size: int = 5):
        self.memory_buffer = []
        self.max_memory_size = max_memory_size
        self.current_problem = None
        self.plan = None
        self.execution_trace = []
    
    def set_problem(self, problem: str):
        """Set current problem"""
        self.current_problem = problem
        self.memory_buffer = []
        self.execution_trace = []
    
    def set_plan(self, plan: List[Dict]):
        """Set execution plan"""
        self.plan = plan
    
    def add_to_memory(self, step: str, result: Any):
        """Add step result to memory"""
        self.memory_buffer.append({
            'step': step,
            'result': result
        })
        
        # Keep only last N items
        if len(self.memory_buffer) > self.max_memory_size:
            self.memory_buffer = self.memory_buffer[-self.max_memory_size:]
    
    def get_memory_summary(self) -> str:
        """Get formatted memory summary"""
        if not self.memory_buffer:
            return "None - this is the first step"
        
        summary = "\n".join([
            f"Step {i+1}: {mem['step']} → Result: {mem['result']}"
            for i, mem in enumerate(self.memory_buffer)
        ])
        return summary
    
    def add_execution_trace(self, trace: Dict):
        """Add execution trace"""
        self.execution_trace.append(trace)
    
    def get_full_trace(self) -> List[Dict]:
        """Get complete execution trace"""
        return self.execution_trace
