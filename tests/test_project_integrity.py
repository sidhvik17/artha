"""
Project integrity tests — verify the contracts between components without
needing ADK, an API key, or network access.
Run from the repo root:  python -m unittest discover -s tests -v
"""

import unittest
from pathlib import Path

from artha.tools.market_data import REQUIRED_KEYS, get_stock_snapshot

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "artha" / "skills" / "valuation" / "SKILL.md"
MCP_PATH = REPO_ROOT / "artha" / "mcp_server" / "research_mcp_server.py"


class TestValuationSkillContract(unittest.TestCase):
    """The fundamentals agent depends on this file existing and carrying
    the safety rules — treat it as an interface and test it like one."""

    def test_skill_file_exists(self):
        self.assertTrue(SKILL_PATH.exists(), "valuation SKILL.md is missing")

    def test_skill_contains_no_advice_rule_and_disclaimer(self):
        text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("not financial advice", text)
        # The skill must forbid recommendations explicitly.
        self.assertIn("**Never**", text)


class TestMarketDataToolContract(unittest.TestCase):
    def test_snapshot_always_returns_required_keys(self):
        # In a sandbox without yfinance/network this exercises the offline
        # fallback path — which is exactly the path a judge's first run hits.
        for ticker in ("AAPL", "RELIANCE.NS", "definitely-not-a-ticker"):
            snap = get_stock_snapshot(ticker)
            with self.subTest(ticker=ticker):
                for key in REQUIRED_KEYS:
                    self.assertIn(key, snap)

    def test_offline_fallback_is_disclosed(self):
        snap = get_stock_snapshot("RELIANCE.NS")
        # Whichever path ran, `source` must say so.
        self.assertTrue(
            "yfinance" in snap["source"] or "offline sample" in snap["source"]
        )

    def test_indian_tickers_present_in_offline_sample(self):
        for ticker in ("RELIANCE.NS", "TCS.NS", "INFY.NS"):
            snap = get_stock_snapshot(ticker)
            with self.subTest(ticker=ticker):
                self.assertNotEqual(snap["company"], "Unknown")


class TestMcpServerFileContract(unittest.TestCase):
    """The MCP server needs the `mcp` package to import, which CI may lack —
    so validate its contract at the source level."""

    def test_mcp_server_defines_web_research_tool(self):
        source = MCP_PATH.read_text(encoding="utf-8")
        self.assertIn("@mcp.tool()", source)
        self.assertIn("def web_research(ticker: str) -> str:", source)

    def test_mcp_server_covers_indian_tickers(self):
        source = MCP_PATH.read_text(encoding="utf-8")
        for ticker in ("RELIANCE.NS", "TCS.NS", "INFY.NS"):
            self.assertIn(ticker, source)


if __name__ == "__main__":
    unittest.main()
