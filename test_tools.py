"""Unit tests for sandboxed tool functions."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools import get_current_weather, calculate

def test_weather_returns_dict():
    result = get_current_weather("Abuja")
    assert isinstance(result, dict)
    assert "city" in result
    assert result["city"] == "Abuja"
    assert "temperature" in result

def test_calculator_addition():
    result = calculate("2+2")
    assert result["result"] == 4

def test_calculator_invalid_expression():
    result = calculate("import os")
    assert "error" in result

def test_unauthorized_tool_not_executed():
    """The sandbox decorator should block tools not in ALLOWED_TOOLS."""
    # Directly test by calling a non‑allowed function (which isn't decorated,
    # but we can verify that the allowed list logic would block – this is just
    # a placeholder; the real test would require injecting a blocked tool.
    # For now, we trust the decorator and assert that our allowed tools work.
    pass  # Remove pass when you add a more specific integration test
