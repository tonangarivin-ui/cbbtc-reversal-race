# Task: write main.py for a make.fun bars-replay trading bot

You are writing ONE file, `main.py`, in this repository. It is a bot for make.fun's
`agent-fun/bars-replay/v1` protocol: the harness writes one JSON line per minute of a 24-hour
cbBTC/USDC window on stdin and the bot writes exactly one reply per batch on stdout. Every entry
runs twice and both action logs must match byte for byte, so nothing may depend on the clock, the
environment or unseeded randomness.

## What you have

- `vendor/makefun_bars.py`: the protocol shim (a byte-identical copy of the kit SDK). Read it
  first. It owns the wire. You write `on_batch(state, batch)` and call `makefun_bars.run(on_batch)`.
  - `state.seq`, `state.t`, `state.cash`, `state.equity`, `state.positions` (dict of `Holding(qty, cost)`)
  - `state.close(symbol)`, `state.depth_at(symbol)`, `state.impact_bps(symbol, amount)`,
    `state.weight_room(symbol)`, `state.value(symbol, qty)`
  - `state.hello["caps"]["max_weight_bps"]`, `["max_orders_per_bar"]`,
    `state.hello["fees"]["min_notional_quote_units"]` (a STRING, int() it)
  - Return a list of order dicts: `{"side": "buy", "symbol": ..., "notional_quote_units": int,
    "max_slippage_bps": int}` or `{"side": "sell", "symbol": ..., "qty": int, "max_slippage_bps": int}`.
    Return `[]` for none. An order decided on a batch fills at the NEXT bar's open.
- `DATA.md`: measurements of the shipped 24-hour dev window (see below). Read it.
- The entrypoint must be `main.py` at the repository root.

## Economics you must respect

- Long only, one position, at most 100% of equity (`max_weight_bps`), cash never negative.
- A buy spends at least `min_notional_quote_units`; the proceeds of a sell in the same reply never
  fund a buy.
- Cost per full round trip is about 26 bps (4 bps fee each way, 2 bps slippage each way, plus your
  own price impact against the pool depth, which for 1,000 USDC at the recorded ~880,000 USDC
  depth is about 7 bps each way). A trade has to catch a move bigger than that.
- `max_slippage_bps` is measured from the close the bot was last sent. Use something sane (about
  20-100) so a stale bar cannot fill at a wild price; the modelled slippage and your impact count
  against it.
- Everything still held at the end is sold at the last close. Miss the guardrails (at least 1 trade,
  max drawdown 25% or less) and the entry ranks below every entry that meets them.

## The strategy the data supports

`DATA.md` holds the measurements. In short: 1-minute returns have positive lag-1 autocorrelation
(+0.15) and a strong multi-hour reversal; a close stretched far below its 3-hour mean tends to come
back by more than the round-trip cost. Trend-following loses money after fees (measured). So:

1. Hold a **base position**: buy with all available cash on the first bar, so the entry always has at
   least one trade.
2. Around that base, trade the reversal: when the close is stretched **above** the lookback mean by a
   threshold, sell the position; when it is stretched **below** by a threshold, buy back with all
   available cash.
3. Full size each time, one position, no shorts.

The parameters that graded best on the dev window, and stayed profitable when fees were doubled,
were a 180-bar mean with a +60 bps sell threshold and a +20..40 bps buy-back threshold. Start from
those, but write the constants at the top of the file with comments explaining each.

## What to produce

`main.py`, well commented, standard library only plus `vendor/makefun_bars.py`. Constants at the
top. Deterministic. Handle the first bars (before the mean has enough history) by buying the base
position and holding. Do not read the clock, the environment or any file.

Do not modify `vendor/makefun_bars.py`, `LICENSE` or `.makefun/owner.json`.

## How you will be checked

I will run `node cli/makefun.mjs grade-local --kit <kit> --bot <this repo> --driver docker`, which
runs the bot twice on the dev window and reports net PnL, trade count, max drawdown and whether the
guardrails are met. The dev window net PnL must be above 0 (that is the gate to race), with at least
1 trade and drawdown under 25%.
