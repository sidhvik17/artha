"""
News / qualitative specialist (course concept: MCP — demonstrated in code).
===========================================================================
Connects to the local MCP server (mcp_server/research_mcp_server.py) over
stdio and uses its `web_research` tool. The agent consumes a tool served over
the Model Context Protocol exactly as it would a third-party MCP server.

NOTE ON ADK VERSIONS: the MCP toolset import path has moved between ADK
releases. This file targets the common pattern (`MCPToolset` +
`StdioServerParameters`). If your installed ADK names these differently,
check the Day 2 codelab's exact import and adjust the marked lines. If MCP
cannot start in your environment, remove `news_agent` from the coordinator's
tool list — the project still demonstrates multiple course concepts
(multi-agent + skills + security) and remains fully functional.
"""

import os
from pathlib import Path

from google.adk.agents import Agent

# --- ADK-version-sensitive imports (adjust per Day 2 codelab if needed) ------
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
# ------------------------------------------------------------------------------

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

_MCP_SERVER = Path(__file__).resolve().parent.parent / "mcp_server" / "research_mcp_server.py"

# Connect to the local MCP server as a stdio subprocess.
research_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=[str(_MCP_SERVER)],
    )
)

news_agent = Agent(
    name="news_agent",
    model=MODEL,
    description=(
        "Gathers recent qualitative notes (catalysts and risks) for a company "
        "via a tool served over the Model Context Protocol."
    ),
    instruction=(
        "You are a qualitative research analyst. When given a ticker, call the "
        "`web_research` tool to retrieve recent notes, then summarise the two "
        "or three most decision-relevant catalysts and risks in plain English. "
        "Make clear these are qualitative notes, not quantitative facts."
    ),
    tools=[research_toolset],
)
