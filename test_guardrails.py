"""Unit tests for responsible AI guardrails."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.guardrails import filter_output

def test_email_redaction():
    text = "Contact me at john.doe@example.com"
    filtered = filter_output(text)
    assert "john.doe@example.com" not in filtered
    assert "[EMAIL]" in filtered

def test_phone_redaction():
    text = "Call 443-322-4915 for info"
    filtered = filter_output(text)
    assert "443-322-4915" not in filtered
    assert "[PHONE]" in filtered

def test_toxic_keyword_blocked():
    text = "I can teach you how to hack into a bank account"
    filtered = filter_output(text)
    assert "I'm sorry" in filtered or "cannot provide" in filtered

def test_clean_text_passes():
    text = "The weather in Abuja is sunny."
    filtered = filter_output(text)
    assert filtered == text
