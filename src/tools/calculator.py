"""
Calculator Tool - Basic Arithmetic Operations
Handles: add, subtract, multiply, divide, percentage, ratio
"""

from typing import List, Union, Dict, Any


class Calculator:
    """Basic arithmetic calculator for agent use"""
    
    def __init__(self):
        self.operations = {
            'add': self._add,
            'subtract': self._subtract,
            'multiply': self._multiply,
            'divide': self._divide,
            'percentage': self._percentage,
            'ratio': self._ratio,
        }
    
    def execute(self, operation: str, operands: List[Union[int, float]]) -> Dict[str, Any]:
        """
        Execute a calculator operation
        
        Args:
            operation: Operation name ('add', 'subtract', etc.)
            operands: List of numbers to operate on
            
        Returns:
            Dict with 'result' and 'success' keys
        """
        try:
            if operation not in self.operations:
                return {
                    'success': False,
                    'error': f"Unknown operation: {operation}",
                    'result': None
                }
            
            if not operands:
                return {
                    'success': False,
                    'error': "No operands provided",
                    'result': None
                }
            
            # Convert all operands to float
            operands = [float(x) for x in operands]
            
            # Execute operation
            result = self.operations[operation](operands)
            
            return {
                'success': True,
                'result': result,
                'operation': operation,
                'operands': operands
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'result': None
            }
    
    def _add(self, operands: List[float]) -> float:
        """Sum all operands"""
        return sum(operands)
    
    def _subtract(self, operands: List[float]) -> float:
        """Subtract all operands from the first"""
        if len(operands) < 2:
            raise ValueError("Subtract requires at least 2 operands")
        result = operands[0]
        for op in operands[1:]:
            result -= op
        return result
    
    def _multiply(self, operands: List[float]) -> float:
        """Multiply all operands"""
        result = 1
        for op in operands:
            result *= op
        return result
    
    def _divide(self, operands: List[float]) -> float:
        """Divide first operand by rest"""
        if len(operands) < 2:
            raise ValueError("Divide requires at least 2 operands")
        if any(op == 0 for op in operands[1:]):
            raise ValueError("Division by zero")
        result = operands[0]
        for op in operands[1:]:
            result /= op
        return result
    
    def _percentage(self, operands: List[float]) -> float:
        """Calculate percentage: operands[0]% of operands[1]"""
        if len(operands) != 2:
            raise ValueError("Percentage requires exactly 2 operands")
        return (operands[0] / 100) * operands[1]
    
    def _ratio(self, operands: List[float]) -> str:
        """Simplify ratio of operands"""
        if len(operands) < 2:
            raise ValueError("Ratio requires at least 2 operands")
        
        from math import gcd
        from functools import reduce
        
        # Convert to integers for GCD
        int_ops = [int(op) for op in operands]
        
        # Find GCD of all numbers
        common_gcd = reduce(gcd, int_ops)
        
        # Simplify
        simplified = [op // common_gcd for op in int_ops]
        
        return ':'.join(map(str, simplified))


# Test function
def test_calculator():
    """Test calculator functionality"""
    calc = Calculator()
    
    tests = [
        ('add', [1, 2, 3], 6),
        ('subtract', [10, 3], 7),
        ('multiply', [2, 3, 4], 24),
        ('divide', [100, 5, 2], 10),
        ('percentage', [25, 200], 50),
        ('ratio', [12, 8], '3:2'),
    ]
    
    print("Testing Calculator:")
    print("-" * 50)
    for operation, operands, expected in tests:
        result = calc.execute(operation, operands)
        status = "✓" if result['success'] else "✗"
        print(f"{status} {operation}({operands}) = {result.get('result', 'ERROR')}")
    

if __name__ == "__main__":
    test_calculator()
