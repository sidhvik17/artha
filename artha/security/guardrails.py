"""
Security guardrail (course concept: Security features — demonstrated in code).
==============================================================================
A `before_model_callback` is ADK's interception point: it runs BEFORE every
call to the LLM. If it returns an `LlmResponse`, the model call is
short-circuited and that response is sent instead — letting us block unsafe
input deterministically, without spending a model call and without trusting
the model to police itself.

The guardrail blocks two classes of input (rules live in detectors.py, which
is pure Python and covered by the unit tests in /tests):
  1. Prompt-injection / system-prompt-exfiltration attempts.
  2. Direct financial-advice solicitation ("should I buy...?") — Artha briefs,
     it never tips, and that rule is enforced structurally, not by vibes.
"""

from __future__ import annotations

from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types

from .detectors import classify

_INJECTION_REPLY = (
    "I can't follow instructions that try to override how I operate. "
    "I can, however, give you a balanced research brief on a stock — "
    "just give me a ticker (e.g. RELIANCE.NS or AAPL)."
)

_ADVICE_REPLY = (
    "I don't give buy/sell recommendations, target prices, or predictions. "
    "What I can do is lay out the fundamentals, recent qualitative notes, and "
    "the key risks so you can decide for yourself. Which ticker would you "
    "like me to brief?\n\n"
    "_This is educational analysis, not financial advice._"
)


def _latest_user_text(llm_request: LlmRequest) -> str:
    """Extract the most recent user message text from the request."""
    contents = getattr(llm_request, "contents", None) or []
    for content in reversed(contents):
        if getattr(content, "role", None) == "user":
            parts = getattr(content, "parts", None) or []
            text = " ".join(p.text for p in parts if getattr(p, "text", None))
            if text:
                return text
    return ""


def _blocked(message: str) -> LlmResponse:
    """Build an LlmResponse that replaces the model call with a safe refusal."""
    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=message)])
    )


def safety_guardrail(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Inspect user input; block injection or advice-seeking before the LLM runs."""
    verdict = classify(_latest_user_text(llm_request))
    if verdict == "injection":
        return _blocked(_INJECTION_REPLY)
    if verdict == "advice":
        return _blocked(_ADVICE_REPLY)
    return None  # input is clean; proceed to the model
