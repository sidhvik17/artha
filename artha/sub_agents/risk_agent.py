"""
Risk specialist  (part of the multi-agent system)
-------------------------------------------------
A pure-reasoning agent (no external tools). The coordinator passes it the
fundamentals read and the qualitative notes, and it produces a concise,
prioritised risk assessment. Including a tool-free specialist keeps the
multi-agent design honest: not every agent needs tools — some add value through
focused reasoning over what the others produced.
"""

import os

from google.adk.agents import Agent

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

risk_agent = Agent(
    name="risk_agent",
    model=MODEL,
    description="Synthesises the most important risks for a company from fundamentals and qualitative notes.",
    instruction=(
        "You are a risk analyst. Given a fundamentals read and qualitative "
        "research notes, identify the THREE most important risks for this "
        "company, ordered by severity. For each, give a one-line explanation and "
        "label it Financial, Operational, Regulatory, Valuation, or Market. "
        "Be specific and avoid generic boilerplate. Do not give advice."
    ),
)
