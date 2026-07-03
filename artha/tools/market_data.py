"""
Function tool: get_stock_snapshot
=================================
Demonstrates an ADK *function tool* (a plain Python function the agent can
call). ADK auto-wraps any function passed in an agent's `tools=[...]` list;
the docstring and type hints below become the tool's schema, so they are kept
accurate deliberately.

Behaviour: try live data from yfinance; on ANY failure (no network, rate
limit, missing package) fall back to a small, clearly-labelled offline sample
so the agent — and a live demo — always produces output. The `source` field
always discloses which path was used; the agent is instructed to report it.
"""

from __future__ import annotations

# Offline dataset. Values are illustrative, NOT live market data.
# Covers both US (plain symbol) and Indian NSE (".NS" suffix) tickers, because
# Artha's target user is the Indian retail investor.
_SAMPLE: dict[str, dict] = {
    "AAPL": {
        "company": "Apple Inc.", "currency": "USD", "price": 231.5,
        "pe_ratio": 35.2, "market_cap": 3_480_000_000_000,
        "profit_margin": 0.246, "revenue_growth_yoy": 0.061,
        "debt_to_equity": 1.45, "sector": "Technology",
    },
    "MSFT": {
        "company": "Microsoft Corporation", "currency": "USD", "price": 449.8,
        "pe_ratio": 37.0, "market_cap": 3_340_000_000_000,
        "profit_margin": 0.358, "revenue_growth_yoy": 0.151,
        "debt_to_equity": 0.33, "sector": "Technology",
    },
    "TCS.NS": {
        "company": "Tata Consultancy Services Ltd.", "currency": "INR",
        "price": 3850.0, "pe_ratio": 28.4, "market_cap": 13_900_000_000_000,
        "profit_margin": 0.192, "revenue_growth_yoy": 0.045,
        "debt_to_equity": 0.09, "sector": "Information Technology",
    },
    "RELIANCE.NS": {
        "company": "Reliance Industries Ltd.", "currency": "INR",
        "price": 2950.0, "pe_ratio": 27.1, "market_cap": 19_900_000_000_000,
        "profit_margin": 0.086, "revenue_growth_yoy": 0.072,
        "debt_to_equity": 0.44, "sector": "Conglomerate / Energy-Retail-Telecom",
    },
    "INFY.NS": {
        "company": "Infosys Ltd.", "currency": "INR",
        "price": 1620.0, "pe_ratio": 24.6, "market_cap": 6_700_000_000_000,
        "profit_margin": 0.166, "revenue_growth_yoy": 0.038,
        "debt_to_equity": 0.10, "sector": "Information Technology",
    },
}

_DEFAULT_SAMPLE = {
    "company": "Unknown", "currency": "USD", "price": None, "pe_ratio": None,
    "market_cap": None, "profit_margin": None, "revenue_growth_yoy": None,
    "debt_to_equity": None, "sector": "Unknown",
}

# Keys every snapshot must contain (the integrity tests assert this contract).
REQUIRED_KEYS = (
    "company", "currency", "price", "pe_ratio", "market_cap",
    "profit_margin", "revenue_growth_yoy", "debt_to_equity", "sector", "source",
)


def get_stock_snapshot(ticker: str) -> dict:
    """Fetch a fundamentals snapshot for a single stock ticker.

    Args:
        ticker: The stock symbol in Yahoo Finance convention — e.g. 'AAPL'
            or 'MSFT' for US listings, 'RELIANCE.NS' or 'TCS.NS' for NSE
            (India) listings.

    Returns:
        A dictionary with keys: company, currency, price, pe_ratio,
        market_cap, profit_margin, revenue_growth_yoy, debt_to_equity,
        sector, and a 'source' field indicating whether the data is live
        (yfinance) or an offline illustrative sample.
    """
    symbol = ticker.strip().upper()

    # Try live data first.
    try:
        import yfinance as yf  # imported lazily so the tool works without it

        info = yf.Ticker(symbol).info
        if info and info.get("currentPrice"):
            return {
                "company": info.get("shortName") or info.get("longName") or symbol,
                "currency": info.get("currency", "USD"),
                "price": info.get("currentPrice"),
                "pe_ratio": info.get("trailingPE"),
                "market_cap": info.get("marketCap"),
                "profit_margin": info.get("profitMargins"),
                "revenue_growth_yoy": info.get("revenueGrowth"),
                "debt_to_equity": (info.get("debtToEquity") / 100.0) if info.get("debtToEquity") else None,
                "sector": info.get("sector", "Unknown"),
                "source": "yfinance (live)",
            }
    except Exception:
        # Any failure (no network, rate limit, missing package) -> fall through.
        pass

    # Offline fallback — always disclosed via `source`.
    base = dict(_SAMPLE.get(symbol, _DEFAULT_SAMPLE))
    base["source"] = "offline sample (illustrative, not live market data)"
    return base
