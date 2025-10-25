"""
Executor Agent - Execute tasks using tools
"""

import json
import re
from typing import Dict, Any
from utils.model_loader import ModelLoader
from utils.rag_retriever import RAGRetriever
from tools.calculator import Calculator
from tools.sympy_solver import SympySolver
from tools.z3_solver import Z3Solver
from tools.pulp_solver import PulpSolver


class ExecutorAgent:
    """Task execution agent with tool usage"""

    def __init__(self, adapter_path: str, rag_retriever: RAGRetriever, model_loader: ModelLoader):
        self.model_loader = model_loader
        self.model = self.model_loader.load_adapter(adapter_path, "executor")
        self.rag = rag_retriever

        self.tools = {
            'calculator': Calculator(),
            'sympy_solver': SympySolver(),
            'z3_solver': Z3Solver(),
            'pulp_solver': PulpSolver()
        }

    def execute(self, task: str, previous_steps_summary: str) -> Dict[str, Any]:
        """
        Execute a task using appropriate tool
        """
        try:
            tool_examples = self.rag.retrieve_tool_examples(task, top_k=2)
            examples_text = "\n\n".join(tool_examples)

            # --- START OF FIX ---
            # A single, raw f-string prompt.
            # We add "<THOUGHT>" at the end to force the model to start responding in the correct format.
            prompt = f"""You are an executor agent. You MUST use one of the available tools.
AVAILABLE TOOLS: calculator, sympy_solver, z3_solver, pulp_solver
You *MUST* and *ONLY* respond in the following format (no other text is allowed):
<THOUGHT>Your reasoning for choosing the tool and arguments</THOUGHT>
<ACTION>tool_name(arguments)</ACTION>

RELEVANT TOOL EXAMPLES:
{examples_text}

PREVIOUS STEPS SUMMARY:
{previous_steps_summary}

CURRENT TASK:
{task}

<THOUGHT>"""
            
            self.model.set_adapter("executor")
            # We add "<THOUGHT>" to the response we get back so the parser doesn't see it
            response = "<THOUGHT>" + self.model_loader.generate(self.model, prompt, max_length=512)
            # --- END OF FIX ---

            tool_call_match = re.search(r"<ACTION>(.+?)</ACTION>", response, re.DOTALL)
            if not tool_call_match:
                return {
                    'success': False,
                    'error': 'No tool action found in response',
                    'tool_used': None,
                    'result': None,
                    'thought': response
                }

            tool_call = tool_call_match.group(1).strip()
            tool_name_match = re.match(r"(\w+)\((.*)\)", tool_call)
            if not tool_name_match:
                return {
                    'success': False,
                    'error': 'Tool call format invalid',
                    'tool_used': None,
                    'result': None,
                    'thought': response
                }

            tool_name = tool_name_match.group(1)
            args_str = tool_name_match.group(2)

            try:
                args = json.loads(f"[{args_str}]")
            except Exception:
                try:
                    args = eval(f"[{args_str}]")
                except Exception as e:
                    return {
                        'success': False,
                        'error': f'Failed to parse arguments: {str(e)}',
                        'tool_used': tool_name,
                        'result': None,
                        'thought': response
                    }

            if tool_name not in self.tools:
                return {
                    'success': False,
                    'error': f"Unknown tool requested: {tool_name}",
                    'tool_used': tool_name,
                    'result': None,
                    'thought': response
                }

            tool = self.tools[tool_name]
            exec_result = tool.execute(*args)

            return {
                'success': True,
                'tool_used': tool_name,
                'result': exec_result.get('result', None),
                'thought': response,
                'input': args,
                'output': exec_result
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'tool_used': None,
                'result': None,
                'thought': ''
            }
