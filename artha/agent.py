"""
Artha — root coordinator agent (course concept: Multi-agent system with ADK).
=============================================================================
ADK looks for `root_agent` in this module. The coordinator orchestrates three
specialist sub-agents (exposed as AgentTools) and is protected by a security
guardrail that runs before every model call.

Course concepts demonstrated in code (capstone requires >= 3):
  1. Multi-agent system with ADK -> coordinator + 3 specialists via AgentTool
  2. MCP server                  -> news_agent consumes a local MCP tool
  3. Agent skills                -> fundamentals_agent loads skills/valuation/SKILL.md
  4. Security features           -> safety_guardrail (before_model_callback),
                                    unit-tested in /tests without an API key
"""

import os

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.fundamentals_agent import fundamentals_agent
from .sub_agents.news_agent import news_agent
from .sub_agents.risk_agent import risk_agent
from .security.guardrails import safety_guardrail

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

root_agent = Agent(
    name="artha_coordinator",
    model=MODEL,
    description=(
        "Coordinates a crew of specialist agents to produce a balanced, "
        "well-sourced equity research brief — never a recommendation."
    ),
    instruction=(
        "You are Artha, the coordinator of an equity-research crew serving "
        "retail investors (many in India — NSE tickers use a '.NS' suffix, "
        "e.g. RELIANCE.NS; US tickers are plain, e.g. AAPL). If the user gives "
        "a company name without a ticker, infer the most likely ticker and say "
        "which one you used.\n\n"
        "SINGLE-STOCK BRIEF — when the user asks about one company:\n"
        "1. Call `fundamentals_agent` with the ticker for the valuation read.\n"
        "2. Call `news_agent` with the ticker for qualitative catalysts/risks.\n"
        "3. Call `risk_agent`, passing it the fundamentals read and the notes, "
        "for a prioritised risk list.\n"
        "4. Synthesise into one brief with sections: **Snapshot**, **Valuation "
        "read**, **Catalysts & qualitative notes**, **Top risks**, and "
        "**Bottom line** (a neutral 'quality vs. price' summary that does NOT "
        "tell the user to buy, sell, or hold).\n\n"
        "COMPARISON — when the user asks to compare two companies:\n"
        "Run steps 1-2 for EACH ticker, then produce a side-by-side comparison "
        "table of the key metrics (P/E, margin, growth, leverage), followed by "
        "a short 'where each is stronger' paragraph and a combined risk note. "
        "Still no recommendation of one over the other as an investment.\n\n"
        "ALWAYS: state the data source (live vs offline sample). End every "
        "response with: 'This is educational analysis, not financial advice.' "
        "If the user asks for a buy/sell call, target price, or prediction, "
        "decline and offer the research brief instead."
    ),
    tools=[
        AgentTool(agent=fundamentals_agent),
        AgentTool(agent=news_agent),
        AgentTool(agent=risk_agent),
    ],
    before_model_callback=safety_guardrail,
)
