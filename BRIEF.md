# Trading bot requirements

Implement the repository's trading entrypoint in `main.py`.
The wire format is `agent-fun/bars-replay/v1`.
For each minute, the harness supplies a JSON line through stdin.
Emit exactly one stdout reply for each batch.
The harness runs the entry twice; the resulting output must be identical byte for byte.

## SDK and state

Use the SDK shim at `vendor/makefun_bars.py`.
It invokes the strategy callback as `on_batch(state, batch)`.
The state exposes these values:

- `seq`: batch sequence.
- `t`: the timestamp supplied by the harness.
- `cash`: available cash.
- `equity`: account equity.
- `positions`: holdings whose `Holding` objects contain `qty` and `cost`.

The state also provides `close()`, `depth_at()`, `impact_bps()`,
`weight_room()`, and `value()` for prices, depth, impact, capacity, and valuation.
Read the position limit from `hello["caps"]["max_weight_bps"]`.
The minimum order value is `hello["fees"]["min_notional_quote_units"]`;
that value arrives as a string and must be converted before numeric use.

## Orders and execution

A buy uses this shape, with integer notional and slippage values:

```python
{"side": "buy", "symbol": symbol, "notional_quote_units": amount, "max_slippage_bps": limit}
```

A sell instead specifies an integer quantity, with an integer slippage limit:

```python
{"side": "sell", "symbol": symbol, "qty": quantity, "max_slippage_bps": limit}
```

Decisions made for the current batch execute at the following bar's open.
Allow only long exposure and a single position.
Position value must stay within `max_weight_bps` of equity, and cash must never go negative.

Budget approximately 26 bps for a complete purchase and sale.
Each direction incurs a 4 bps fee and 2 bps of slippage, plus pool price impact.
At the recorded depth, an order of 1,000 USDC adds about 7 bps of impact per direction.
The `max_slippage_bps` limit is relative to the last close delivered to the bot.
Keep that limit modest to prevent an old bar from authorizing execution at an extreme price.

Any remaining holdings are liquidated at the final close.
An entry must execute at least one trade and keep maximum drawdown at or below 25%.
Entries that fail either guardrail rank below every entry that satisfies both.

## Strategy to implement

Establish a base holding by buying on the first bar, ensuring the entry has a trade.
Use a multi-hour reversal overlay around that initial exposure.
Sell when the close sits sufficiently above its lookback average.
After selling, wait to buy back until the close is sufficiently below that average.
Merely remaining out of the market is not a buy signal.

The best graded parameters also remained profitable when fees were doubled:

- Compute the mean over 180 bars.
- Sell at a stretch of +60 bps above the mean.
- Buy back at a stretch of 40 bps below the mean, the +40 bps buy-back parameter.

Use only the standard library and the supplied shim.
Do not consult a clock, environment variables, or files.
