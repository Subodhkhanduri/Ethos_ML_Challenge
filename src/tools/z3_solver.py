"""
Z3 Solver Tool - Constraint Satisfaction Problems
Handles: logical constraints, integer constraints, optimization
"""

from typing import List, Dict, Any
from z3 import *


class Z3Solver:
    """Constraint satisfaction solver using Z3"""
    
    def __init__(self):
        pass
    
    def execute(self, constraints: List[str], variables: Dict[str, str]) -> Dict[str, Any]:
        """
        Solve constraint satisfaction problem
        
        Args:
            constraints: List of constraint strings (e.g., ['x + y > 10', 'x < 5'])
            variables: Dict of {var_name: type} where type is 'int', 'real', or 'bool'
            
        Returns:
            Dict with 'result' (variable assignments) and 'success' keys
        """
        try:
            if not constraints:
                return {
                    'success': False,
                    'error': "No constraints provided",
                    'result': None
                }
            
            if not variables:
                return {
                    'success': False,
                    'error': "No variables specified",
                    'result': None
                }
            
            # Create solver
            solver = Solver()
            
            # Create Z3 variables
            z3_vars = {}
            for var_name, var_type in variables.items():
                if var_type == 'int':
                    z3_vars[var_name] = Int(var_name)
                elif var_type == 'real':
                    z3_vars[var_name] = Real(var_name)
                elif var_type == 'bool':
                    z3_vars[var_name] = Bool(var_name)
                else:
                    return {
                        'success': False,
                        'error': f"Unknown variable type: {var_type}",
                        'result': None
                    }
            
            # Add constraints
            for constraint_str in constraints:
                try:
                    # Replace variable names with Z3 variables in expression
                    constraint_expr = constraint_str
                    for var_name in z3_vars:
                        constraint_expr = constraint_expr.replace(var_name, f"z3_vars['{var_name}']")
                    
                    # Evaluate to get Z3 constraint
                    constraint = eval(constraint_expr, {"z3_vars": z3_vars, "__builtins__": {}})
                    solver.add(constraint)
                    
                except Exception as e:
                    return {
                        'success': False,
                        'error': f"Failed to parse constraint '{constraint_str}': {str(e)}",
                        'result': None
                    }
            
            # Solve
            if solver.check() == sat:
                model = solver.model()
                
                # Extract solution
                solution = {}
                for var_name, var in z3_vars.items():
                    val = model[var]
                    if val is not None:
                        # Convert Z3 value to Python type
                        if variables[var_name] == 'int':
                            solution[var_name] = val.as_long()
                        elif variables[var_name] == 'real':
                            solution[var_name] = float(val.as_decimal(10))
                        elif variables[var_name] == 'bool':
                            solution[var_name] = bool(val)
                        else:
                            solution[var_name] = str(val)
                
                return {
                    'success': True,
                    'result': solution,
                    'constraints': constraints
                }
            else:
                return {
                    'success': False,
                    'error': "No solution satisfies all constraints",
                    'result': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Z3 solver error: {str(e)}",
                'result': None
            }


# Test function
def test_z3_solver():
    """Test Z3 solver functionality"""
    solver = Z3Solver()
    
    tests = [
        # (constraints, variables, description)
        (
            ['x + y == 10', 'x > 3'],
            {'x': 'int', 'y': 'int'},
            "Integer constraints"
        ),
        (
            ['x + y >= 10', 'x < 7', 'y < 8'],
            {'x': 'int', 'y': 'int'},
            "Multiple inequalities"
        ),
        (
            ['a or b', 'not (a and b)'],
            {'a': 'bool', 'b': 'bool'},
            "Boolean logic"
        ),
    ]
    
    print("Testing Z3 Solver:")
    print("-" * 50)
    for constraints, variables, desc in tests:
        result = solver.execute(constraints, variables)
        status = "✓" if result['success'] else "✗"
        print(f"{status} {desc}: {result.get('result', 'ERROR')}")


if __name__ == "__main__":
    test_z3_solver()
