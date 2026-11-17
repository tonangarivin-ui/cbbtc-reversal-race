import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars


SYMBOL = "CBBTC"  # The traded cbBTC/USDC market.
LOOKBACK = 180  # Bars in the mean that defines an extreme stretch.
SELL_STRETCH_BPS = 60  # Exit the base position this far above the mean.
BUY_STRETCH_BPS = 40  # Re-enter this far below the mean.
MAX_SLIPPAGE_BPS = 100  # Reject fills that move too far from the last close.
FEE_BPS = 4  # Reserve one buy-side fee so the account never overspends cash.

closes = []


def on_batch(state, batch):
    close = state.close(SYMBOL)
    if close is None:
        return []

    closes.append(close)
    if len(closes) > LOOKBACK:
        del closes[0]

    holding = state.positions.get(SYMBOL)
    if holding is None:
        if state.warming_up:
            return []
        notional = min(state.cash * 10_000 // (10_000 + FEE_BPS), state.weight_room(SYMBOL))
        minimum = int(state.hello["fees"]["min_notional_quote_units"])
        if notional < minimum:
            return []
        return [{
            "side": "buy",
            "symbol": SYMBOL,
            "notional_quote_units": notional,
            "max_slippage_bps": MAX_SLIPPAGE_BPS,
        }]

    if len(closes) < LOOKBACK:
        return []

    mean = sum(closes) // LOOKBACK
    stretch_bps = (close - mean) * 10_000 // mean
    if stretch_bps >= SELL_STRETCH_BPS:
        return [{
            "side": "sell",
            "symbol": SYMBOL,
            "qty": holding.qty,
            "max_slippage_bps": MAX_SLIPPAGE_BPS,
        }]

    if stretch_bps <= -BUY_STRETCH_BPS:
        notional = min(state.cash * 10_000 // (10_000 + FEE_BPS), state.weight_room(SYMBOL))
        minimum = int(state.hello["fees"]["min_notional_quote_units"])
        if notional >= minimum:
            return [{
                "side": "buy",
                "symbol": SYMBOL,
                "notional_quote_units": notional,
                "max_slippage_bps": MAX_SLIPPAGE_BPS,
            }]

    return []


makefun_bars.run(on_batch)
