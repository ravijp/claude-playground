def calculate(expression):
    """Safe calculator"""
    try:
        # Simple eval - use safer alternatives in production
        allowed_names = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'pow': pow
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"
