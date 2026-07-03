"""
Fundamentals specialist (course concept: Agent skills — demonstrated in code).
==============================================================================
- Uses the `get_stock_snapshot` function tool to fetch the numbers.
- Loads the valuation Agent Skill (skills/valuation/SKILL.md) into its
  instruction, so it reasons with a consistent, disclosed methodology instead
  of ad-hoc vibes. This is the SKILL.md progressive-disclosure pattern from
  the course: the methodology lives in a versioned markdown file, is loaded
  only where needed, and can be improved without touching agent code.
"""

import os
from pathlib import Path

from google.adk.agents import Agent

from ..tools.market_data import get_stock_snapshot

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

# Load the valuation skill from disk at construction time.
_SKILL_PATH = Path(__file__).resolve().parent.parent / "skills" / "valuation" / "SKILL.md"
_VALUATION_SKILL = _SKILL_PATH.read_text(encoding="utf-8") if _SKILL_PATH.exists() else ""

fundamentals_agent = Agent(
    name="fundamentals_agent",
    model=MODEL,
    description=(
        "Fetches a fundamentals snapshot and reads valuation, profitability, "
        "growth, and leverage using a disclosed SKILL.md methodology."
    ),
    instruction=(
        "You are an equity fundamentals analyst. When given a ticker, call "
        "`get_stock_snapshot` to retrieve the numbers, then analyse them by "
        "strictly following the skill below. Always report the data `source` "
        "field so the reader knows whether numbers are live or sample.\n\n"
        "===== SKILL: VALUATION READING =====\n"
        f"{_VALUATION_SKILL}\n"
        "===== END SKILL ====="
    ),
    tools=[get_stock_snapshot],
)
