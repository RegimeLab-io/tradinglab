# RegimeLab — Documentation

## Architecture

The RegimeLab trading bot consists of three layers:

**1. Data layer**
- Market data via IBKR
- News sentiment feeds
- Earnings calendar (Finnhub)

**2. Agent layer**
- 10 specialized Claude Code agents
- Shared memory and skill files
- Guardian agent closes the learning loop

**3. Execution layer**
- Decision engine applies regime-specific parameters
- Orders routed via ib_insync to Interactive Brokers
- TimescaleDB logs every trade with regime label

## Regime detection

The bot classifies market conditions using SPY EMA and VIX:

| Regime | Condition |
|---|---|
| BULL | SPY above EMA26w, VIX below 20 |
| NEUTRAL | SPY near EMA26w, VIX 20-30 |
| BEAR | SPY below EMA26w, VIX above 30 |
| TURBULENT | VIX spike, uses BEAR parameters |

Each regime has its own Optuna parameter study — optimized independently.

## Learning loop

Every trade outcome flows back into the system:
1. Guardian agent reads trade result
2. Patterns identified (e.g. CHASING_MOMENTUM, ticker bias)
3. Learning filter blocks losing patterns in future entries
4. Skill files updated nightly

→ [Join the waitlist at regimelab.dev](https://regimelab.dev) for full documentation
