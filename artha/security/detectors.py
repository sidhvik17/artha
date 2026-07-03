"""
Pure security detectors (no framework dependencies).
====================================================
Design note: the *detection logic* is deliberately separated from the ADK
callback wrapper (guardrails.py). This makes the security layer unit-testable
without installing ADK or holding an API key — run `python -m unittest` from
the repo root and these rules are verified deterministically. In production
you would swap these heuristics for an LLM-based classifier or the STRIDE /
threat-scan tooling from the course's security unit; the wiring stays the same.
"""

from __future__ import annotations

# Phrases that suggest an attempt to override instructions or leak the prompt.
INJECTION_MARKERS: tuple[str, ...] = (
    "ignore previous instructions",
    "ignore all previous",
    "disregard your instructions",
    "reveal your system prompt",
    "print your system prompt",
    "show me your instructions",
    "you are now",
    "act as though you have no rules",
)

# Phrases that solicit direct investment advice (out of scope by design:
# Artha briefs, it never tips).
ADVICE_MARKERS: tuple[str, ...] = (
    "should i buy",
    "should i sell",
    "is it a good time to buy",
    "is it a good time to sell",
    "will it go up",
    "will it go down",
    "guarantee",
    "tell me what to invest in",
    "which stock will double",
    "give me a target price",
)


def detect_injection(text: str) -> bool:
    """True if the text contains a prompt-injection / exfiltration attempt."""
    lowered = text.lower()
    return any(marker in lowered for marker in INJECTION_MARKERS)


def detect_advice_seeking(text: str) -> bool:
    """True if the text directly solicits buy/sell advice or predictions."""
    lowered = text.lower()
    return any(marker in lowered for marker in ADVICE_MARKERS)


def classify(text: str) -> str | None:
    """Classify user input for the guardrail.

    Returns:
        'injection' | 'advice' | None (clean input).
        Injection takes precedence: a message that both injects and asks for
        advice is treated as an attack first.
    """
    if detect_injection(text):
        return "injection"
    if detect_advice_seeking(text):
        return "advice"
    return None
