# Examples

Sample outputs from the RegimeLab trading bot.

## Backtest output (sample)
```json
{
  "regime": "BULL",
  "period": "2024-01 to 2024-06",
  "trades": 47,
  "win_rate": 0.62,
  "avg_profit": 1.84,
  "avg_loss": -0.91,
  "profit_factor": 1.38,
  "max_drawdown": -4.2,
  "sharpe": 1.12
}
```

## Walk-forward validation (sample)

| Period | Regime | Win Rate | Profit Factor | Sharpe |
|---|---|---|---|---|
| Q1 2024 | BULL | 64% | 1.42 | 1.18 |
| Q2 2024 | NEUTRAL | 51% | 1.09 | 0.61 |
| Q3 2024 | BEAR | 58% | 1.31 | 0.94 |
| Q4 2024 | BULL | 67% | 1.55 | 1.34 |

## Regime distribution (sample)

| Regime | % of time | Avg trades/week |
|---|---|---|
| BULL | 58% | 12 |
| NEUTRAL | 31% | 7 |
| BEAR | 9% | 4 |
| TURBULENT | 2% | 1 |

---

*Sample data for illustration. Real results available to members.*

→ [Join the waitlist at regimelab.dev](https://regimelab.dev)
