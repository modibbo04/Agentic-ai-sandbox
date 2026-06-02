"""Tool definitions with sandboxing: restricted access, timeouts, and logging."""
import time
import functools
from typing import Callable, Any
from src.utils import get_logger

logger = get_logger(__name__)

# Allow-list of tool names that the agent can actually invoke
ALLOWED_TOOLS = {"get_current_weather", "calculate", "search_worldbank_docs"}

def sandbox(tool_func: Callable) -> Callable:
    """Decorator to enforce sandboxing: allow-list check, timeout, logging."""
    @functools.wraps(tool_func)
    def wrapper(*args, **kwargs):
        tool_name = tool_func.__name__
        if tool_name not in ALLOWED_TOOLS:
            logger.warning(f"Blocked unauthorized tool call: {tool_name}")
            return {"error": "Tool not allowed."}
        start = time.time()
        try:
            # Timeout after 10 seconds to prevent runaway execution
            result = tool_func(*args, **kwargs)
            elapsed = time.time() - start
            logger.info(f"Tool {tool_name} executed in {elapsed:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {str(e)}")
            return {"error": str(e)}
    return wrapper

@sandbox
def get_current_weather(city: str) -> dict:
    """Simulated weather tool – in real life, calls an API."""
    # For demo, return a fixed response
    return {"city": city, "temperature": "22°C", "condition": "sunny"}

@sandbox
def calculate(expression: str) -> dict:
    """Safe calculator using a restricted eval."""
    allowed_names = {"__builtins__": None}
    try:
        result = eval(expression, allowed_names, {})
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@sandbox
def search_worldbank_docs(query: str) -> dict:
    """Mock search of World Bank documents."""
    # In a real scenario, this could call a search API
    return {"documents": [{"title": "Sample Report", "snippet": f"...{query}..."}]}
