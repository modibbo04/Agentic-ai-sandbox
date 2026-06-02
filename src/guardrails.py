"""Responsible AI guardrails: output filtering, PII detection, toxicity checks."""
import re
from src.utils import get_logger

logger = get_logger(__name__)

def filter_output(text: str) -> str:
    """Apply safety guardrails to LLM output."""
    # 1. Simple PII redaction (emails, phone numbers)
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)

    # 2. Block known toxic patterns (placeholder)
    toxic_keywords = ["hack", "exploit vulnerability", "illegal"]
    for word in toxic_keywords:
        if word in text.lower():
            logger.warning(f"Toxic content detected: {word}")
            return "I'm sorry, I cannot provide that information."

    return text
