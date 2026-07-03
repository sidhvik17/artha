"""
Local MCP server (course concept: MCP Server — demonstrated in code).
=====================================================================
A real Model Context Protocol server built with FastMCP. It exposes one tool,
`web_research`, which the news_agent connects to over stdio. ADK talks to this
exactly the way it would talk to any third-party MCP server (a news API, the
Google Developer Knowledge MCP server from Day 2, a database) — the only
difference is this one is local and self-contained, so the project runs and
records without external API keys. To go live later, replace the body of
`web_research` with a call to a search/news API; the agent side is unchanged.

Sanity-check standalone:  python research_mcp_server.py
(it waits on stdio — that's correct; ADK drives it as a subprocess.)
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("artha-research")

# Curated, clearly-labelled qualitative notes. Replace with a live API in prod.
_NOTES = {
    "AAPL": [
        "Services revenue continues to grow double digits, improving margin mix.",
        "Regulatory scrutiny over App Store fees in the EU remains an open risk.",
        "Hardware refresh cycle and AI feature rollout are key near-term catalysts.",
    ],
    "MSFT": [
        "Cloud (Azure) growth is the primary driver; AI capacity demand is strong.",
        "Capex on data centres is rising sharply, pressuring free cash flow.",
        "Enterprise Copilot adoption is an emerging monetisation lever.",
    ],
    "TCS.NS": [
        "Large-deal TCV remains healthy though discretionary IT spend is soft.",
        "Strong, near debt-free balance sheet supports dividends and buybacks.",
        "Margin defence amid wage hikes and currency moves is the watch item.",
    ],
    "RELIANCE.NS": [
        "Retail and Jio now drive a growing share of earnings versus energy.",
        "New-energy capex (solar, batteries) is a long-dated optionality bet.",
        "Conglomerate structure keeps a holding-company discount in play.",
    ],
    "INFY.NS": [
        "Deal pipeline steady; clients prioritising cost-takeout programmes.",
        "GenAI service lines are early but strategically important.",
        "Attrition has normalised, supporting margin stability.",
    ],
}

_GENERIC = [
    "No company-specific research notes are available in the local sample set.",
    "Treat the fundamentals snapshot as the primary evidence for this name.",
]


@mcp.tool()
def web_research(ticker: str) -> str:
    """Return recent qualitative research notes for a company by ticker.

    Args:
        ticker: Stock symbol, e.g. 'AAPL', 'RELIANCE.NS', or 'TCS.NS'.

    Returns:
        A short bulleted string of qualitative notes (catalysts and risks),
        clearly labelled as coming from the local sample set.
    """
    symbol = ticker.strip().upper()
    notes = _NOTES.get(symbol, _GENERIC)
    header = f"Qualitative research notes for {symbol} (local MCP sample):"
    return header + "\n- " + "\n- ".join(notes)


if __name__ == "__main__":
    # Default transport is stdio, which is what ADK's StdioServerParameters uses.
    mcp.run()
