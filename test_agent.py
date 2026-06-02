"""Tests for agent parsing logic (no LLM required)."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import Agent

def test_parse_tool_call_valid():
    agent = Agent(model="llama3.2")  # not used; just to access the method
    text = "TOOL: get_current_weather(city='Abuja')"
    tool_name, args = agent._parse_tool_call(text)
    assert tool_name == "get_current_weather"
    assert args == {"city": "Abuja"}

def test_parse_tool_call_no_args():
    text = "TOOL: calculate()"
    name, args = agent._parse_tool_call(text)
    assert name == "calculate"
    assert args == {}

def test_parse_tool_call_not_found():
    text = "I think the answer is 42."
    result = agent._parse_tool_call(text)
    assert result is None

def test_parse_tool_call_multiple_args():
    text = "TOOL: search_worldbank_docs(query='poverty reduction', limit='5')"
    name, args = agent._parse_tool_call(text)
    assert name == "search_worldbank_docs"
    assert args["query"] == "poverty reduction"
    assert args["limit"] == "5"
