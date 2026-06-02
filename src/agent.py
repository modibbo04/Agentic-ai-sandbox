"""Agentic AI: reasoning loop that calls tools based on LLM output."""
import json
import re
from typing import List, Dict, Any
from langchain_ollama import ChatOllama  # requires langchain-ollama
from src.tools import ALLOWED_TOOLS, get_current_weather, calculate, search_worldbank_docs
from src.guardrails import filter_output
from src.utils import get_logger

logger = get_logger(__name__)

# Mapping of tool names to functions
TOOL_MAP = {
    "get_current_weather": get_current_weather,
    "calculate": calculate,
    "search_worldbank_docs": search_worldbank_docs,
}

class Agent:
    def __init__(self, model: str = "llama3.2", temperature: float = 0.0):
        self.llm = ChatOllama(model=model, temperature=temperature)

    def run(self, user_query: str, max_steps: int = 5) -> str:
        """Execute the agent loop with a user query."""
        messages = [{"role": "user", "content": user_query}]
        step = 0
        while step < max_steps:
            response = self.llm.invoke(messages)
            content = response.content.strip()
            logger.info(f"Agent step {step}: {content[:100]}...")

            # Check if the LLM wants to call a tool (simple pattern: TOOL: name(args))
            tool_call = self._parse_tool_call(content)
            if tool_call:
                tool_name, tool_args = tool_call
                if tool_name in TOOL_MAP:
                    logger.info(f"Calling tool: {tool_name}")
                    tool_result = TOOL_MAP[tool_name](**tool_args)
                    # Feed the tool result back into the conversation
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "system", "content": f"Tool result: {json.dumps(tool_result)}"})
                else:
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "system", "content": "Error: Tool not allowed."})
            else:
                # Final answer – apply guardrails and return
                safe_content = filter_output(content)
                return safe_content
            step += 1
        return "I wasn't able to complete the task within the step limit."

    def _parse_tool_call(self, text: str):
        """Simple parser for tool calls: TOOL: name(key=value)"""
        match = re.match(r"TOOL:\s*(\w+)\(([^)]*)\)", text)
        if match:
            name = match.group(1)
            args_str = match.group(2)
            args = {}
            if args_str:
                for pair in args_str.split(","):
                    key, val = pair.split("=")
                    args[key.strip()] = val.strip().strip("'\"")
            return name, args
        return None
