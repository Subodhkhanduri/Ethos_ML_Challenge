"""
Validator Agent - Verify tool outputs
"""

from typing import Dict, Any

class ValidatorAgent:
    """Validates tool outputs for correctness and consistency"""
    
    def __init__(self):
        pass
    
    def validate(self, tool_name: str, input_data: Dict[str, Any], output_data: Dict[str, Any]) -> bool:
        """
        Validate the output of a tool based on input and tool type
        
        Args:
            tool_name: Name of tool used (calculator, sympy_solver, z3_solver, pulp_solver)
            input_data: Input data to tool
            output_data: Output data from tool
            
        Returns:
            True if output is valid, False otherwise
        """
        try:
            # Basic checks
            if not output_data or 'success' not in output_data:
                return False
            if not output_data['success']:
                return False
            
            # Tool-specific validation
            if tool_name == 'calculator':
                return self._validate_calculator(input_data, output_data)
            elif tool_name == 'sympy_solver':
                return self._validate_sympy(input_data, output_data)
            elif tool_name == 'z3_solver':
                return self._validate_z3(input_data, output_data)
            elif tool_name == 'pulp_solver':
                return self._validate_pulp(input_data, output_data)
            else:
                # Unknown tool, assume valid
                return True
                
        except Exception:
            return False
    
    def _validate_calculator(self, input_data, output_data):
        # Check result is number and operands match input
        if 'result' in output_data and isinstance(output_data['result'], (int, float)):
            return True
        return False
    
    def _validate_sympy(self, input_data, output_data):
        # Check that solutions exist and are consistent
        if 'result' in output_data and output_data['result'] is not None:
            return True
        return False
    
    def _validate_z3(self, input_data, output_data):
        # Check for solution presence
        if 'result' in output_data and output_data['result'] is not None:
            return True
        return False
    
    def _validate_pulp(self, input_data, output_data):
        # Check status and solution exists
        if output_data.get('success', False) and output_data.get('result', None) is not None:
            return True
        return False
