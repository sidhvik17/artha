# Skill: Equity Valuation Reading

## Purpose
Turn a raw fundamentals snapshot into a clear, balanced, plain-English read of a
company's quality and valuation — without ever issuing a buy/sell recommendation.

## When to use
Whenever you have a fundamentals snapshot (price, P/E, margin, growth, leverage)
and need to explain what it implies about business quality and how richly the
stock is priced.

## Method (follow in order)
1. **Valuation vs. sector.** Compare the trailing P/E to a rough sector norm
   (Tech ~25-35x, IT Services ~20-30x, Consumer Staples ~18-25x). State whether
   the stock looks cheap, in-line, or rich *relative to its sector*, and say so
   explicitly rather than in absolute terms.
2. **Profitability.** Read `profit_margin`. >20% is strong, 10-20% is healthy,
   <10% is thin or cyclical. Note the level plainly.
3. **Growth.** Read `revenue_growth_yoy`. >15% is high growth, 5-15% is steady,
   <5% or negative is mature/declining. Pair growth with valuation: a high P/E is
   only justified by high growth.
4. **Balance sheet.** Read `debt_to_equity`. <0.5 is conservative, 0.5-1.5 is
   moderate, >1.5 is leveraged (higher risk in downturns).
5. **Synthesis.** In 2-3 sentences, combine the four readings into an overall
   "quality vs. price" picture. Flag the single biggest tension (e.g. "high
   quality but priced for perfection").

## Output rules
- Be specific and cite the numbers you used.
- Always present at least one positive and one risk.
- **Never** say "buy", "sell", "hold", or "this is a good investment". You
  describe; the human decides.
- End every valuation read with this exact line:
  > _This is educational analysis, not financial advice._
