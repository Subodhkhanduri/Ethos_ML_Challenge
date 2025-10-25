"""
SymPy Solver Tool - Algebraic Equation Solving
Handles: single equations, systems of equations, symbolic math
"""

from typing import List, Dict, Any
import sympy as sp
from sympy import symbols, solve, Eq, sympify


class SympySolver:
    """Algebraic equation solver using SymPy"""
    
    def __init__(self):
        pass
    
    def execute(self, equations: List[str], variables: List[str]) -> Dict[str, Any]:
        """
        Solve algebraic equations
        
        Args:
            equations: List of equation strings (e.g., ['x + 5 - 10', 'x**2 - 4'])
            variables: List of variable names to solve for (e.g., ['x', 'y'])
            
        Returns:
            Dict with 'result' (solutions) and 'success' keys
        """
        try:
            if not equations:
                return {
                    'success': False,
                    'error': "No equations provided",
                    'result': None
                }
            
            if not variables:
                return {
                    'success': False,
                    'error': "No variables specified",
                    'result': None
                }
            
            # Create symbolic variables
            var_symbols = symbols(' '.join(variables))
            if len(variables) == 1:
                var_symbols = [var_symbols]
            else:
                var_symbols = list(var_symbols)
            
            # Parse equations
            sympy_eqs = []
            for eq_str in equations:
                try:
                    # Parse as expression (assumed equal to 0)
                    expr = sympify(eq_str, locals={v: var_symbols[i] for i, v in enumerate(variables)})
                    sympy_eqs.append(expr)
                except Exception as e:
                    return {
                        'success': False,
                        'error': f"Failed to parse equation '{eq_str}': {str(e)}",
                        'result': None
                    }
            
            # Solve
            if len(sympy_eqs) == 1 and len(var_symbols) == 1:
                # Single equation, single variable
                solutions = solve(sympy_eqs[0], var_symbols[0])
            else:
                # System of equations
                solutions = solve(sympy_eqs, var_symbols)
            
            # Format solutions
            formatted_solutions = self._format_solutions(solutions, variables)
            
            return {
                'success': True,
                'result': formatted_solutions,
                'equations': equations,
                'variables': variables
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Solver error: {str(e)}",
                'result': None
            }
    
    def _format_solutions(self, solutions, variables):
        """Format SymPy solutions to readable dict"""
        if isinstance(solutions, dict):
            # System solution as dict
            return {str(k): float(v) if v.is_number else str(v) for k, v in solutions.items()}
        elif isinstance(solutions, list):
            if len(solutions) == 0:
                return "No solution"
            elif len(variables) == 1:
                # Single variable, multiple solutions
                return [float(sol) if sol.is_number else str(sol) for sol in solutions]
            else:
                # Multiple solutions for system
                formatted = []
                for sol in solutions:
                    if isinstance(sol, dict):
                        formatted.append({str(k): float(v) if v.is_number else str(v) for k, v in sol.items()})
                    elif isinstance(sol, tuple):
                        formatted.append({variables[i]: float(sol[i]) if sol[i].is_number else str(sol[i]) for i in range(len(sol))})
                    else:
                        formatted.append(float(sol) if sol.is_number else str(sol))
                return formatted
        else:
            # Single solution
            return float(solutions) if solutions.is_number else str(solutions)


# Test function
def test_sympy_solver():
    """Test SymPy solver functionality"""
    solver = SympySolver()
    
    tests = [
        # (equations, variables, description)
        (['x + 5 - 10'], ['x'], "Simple linear"),
        (['x**2 - 4'], ['x'], "Quadratic"),
        (['x + y - 10', 'x - y - 2'], ['x', 'y'], "System 2x2"),
        (['2*x + 3*y - 12', 'x - y - 1'], ['x', 'y'], "Linear system"),
    ]
    
    print("Testing SymPy Solver:")
    print("-" * 50)
    for equations, variables, desc in tests:
        result = solver.execute(equations, variables)
        status = "✓" if result['success'] else "✗"
        print(f"{status} {desc}: {result.get('result', 'ERROR')}")


if __name__ == "__main__":
    test_sympy_solver()
