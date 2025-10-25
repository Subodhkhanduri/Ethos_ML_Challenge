"""
PuLP Solver Tool - Linear Programming Optimization
Handles: linear optimization, resource allocation, scheduling
"""

from typing import List, Dict, Any
import pulp


class PulpSolver:
    
    def __init__(self):
        pass
    
    def execute(self, objective: str, constraints: List[str], 
                variables: Dict[str, Dict[str, Any]], sense: str = 'maximize') -> Dict[str, Any]:
        """
        Solve linear programming problem
        
        Args:
            objective: Objective function string (e.g., '3*x + 5*y')
            constraints: List of constraint strings (e.g., ['x + y <= 10', '2*x + y <= 15'])
            variables: Dict of {var_name: {'low_bound': val, 'up_bound': val, 'cat': 'Integer'/'Continuous'}}
            sense: 'maximize' or 'minimize'
            
        Returns:
            Dict with 'result' (optimal values) and 'success' keys
        """
        try:
            # Create problem
            if sense.lower() == 'maximize':
                prob = pulp.LpProblem("OptimizationProblem", pulp.LpMaximize)
            else:
                prob = pulp.LpProblem("OptimizationProblem", pulp.LpMinimize)
            
            # Create variables
            lp_vars = {}
            for var_name, var_props in variables.items():
                low_bound = var_props.get('low_bound', None)
                up_bound = var_props.get('up_bound', None)
                cat = var_props.get('cat', 'Continuous')
                
                if cat.lower() == 'integer':
                    lp_vars[var_name] = pulp.LpVariable(var_name, lowBound=low_bound, 
                                                         upBound=up_bound, cat='Integer')
                else:
                    lp_vars[var_name] = pulp.LpVariable(var_name, lowBound=low_bound, 
                                                         upBound=up_bound, cat='Continuous')
            
            # Set objective
            obj_expr = self._parse_expression(objective, lp_vars)
            prob += obj_expr
            
            # Add constraints
            for constraint_str in constraints:
                constraint = self._parse_constraint(constraint_str, lp_vars)
                prob += constraint
            
            # Solve
            prob.solve(pulp.PULP_CBC_CMD(msg=0))
            
            # Check status
            if pulp.LpStatus[prob.status] == 'Optimal':
                solution = {var.name: var.varValue for var in prob.variables()}
                
                return {
                    'success': True,
                    'result': solution,
                    'objective_value': pulp.value(prob.objective),
                    'status': 'Optimal'
                }
            else:
                return {
                    'success': False,
                    'error': f"Solver status: {pulp.LpStatus[prob.status]}",
                    'result': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"PuLP solver error: {str(e)}",
                'result': None
            }
    
    def _parse_expression(self, expr_str: str, variables: Dict) -> Any:
        """Parse expression string to PuLP expression"""
        expr = expr_str
        for var_name in variables:
            expr = expr.replace(var_name, f"variables['{var_name}']")
        return eval(expr, {"variables": variables, "__builtins__": {}})
    
    def _parse_constraint(self, constraint_str: str, variables: Dict) -> Any:
        """Parse constraint string to PuLP constraint"""
        # Replace variable names
        expr = constraint_str
        for var_name in variables:
            expr = expr.replace(var_name, f"variables['{var_name}']")
        return eval(expr, {"variables": variables, "__builtins__": {}})


# Test
def test_pulp_solver():
    solver = PulpSolver()
    result = solver.execute(
        objective='3*x + 5*y',
        constraints=['x + y <= 10', '2*x + y <= 15'],
        variables={'x': {'low_bound': 0, 'cat': 'Continuous'}, 
                   'y': {'low_bound': 0, 'cat': 'Continuous'}},
        sense='maximize'
    )
    print(f"PuLP Test: {result}")

if __name__ == "__main__":
    test_pulp_solver()
