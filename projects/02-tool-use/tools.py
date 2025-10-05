"""Tool definitions for Claude"""

def get_weather(location):
    """Simulated weather API"""
    # In real scenario, call actual weather API
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F",
        "London": "Rainy, 58°F",
        "Tokyo": "Clear, 75°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")

def calculate(expression):
    """Safe calculator"""
    try:
        # Simple eval for demo - in production use safer alternatives
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"

# Tool definitions for Claude
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name, e.g., San Francisco"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform a mathematical calculation",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g., '2 + 2' or '10 * 5'"
                }
            },
            "required": ["expression"]
        }
    }
]

# Map tool names to functions
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "calculate": calculate
}
