# RegimeLab Agents

This directory contains the Claude Code agent definitions for the RegimeLab trading bot.

## Agent overview

| Agent | Role |
|---|---|
| `trading-architect` | Orchestrator — coordinates all other agents |
| `regime-detector` | Detects market regime: BULL, NEUTRAL, BEAR, TURBULENT |
| `guardian-agent` | Monitors bot behavior, writes learnings to skill files |
| `risk-manager` | Position sizing, drawdown limits, conviction scoring |
| `backtesting-integrity` | Walk-forward validation, overfitting detection |
| `optuna-optimizer` | Regime-specific parameter optimization |
| `learning-agent` | Processes trade outcomes, updates decision filters |
| `news-sentiment` | Market sentiment from news feeds |
| `earnings-calendar` | Filters trades around earnings events |
| `microstructure` | Slippage estimation, transaction cost modeling |
| `performance-attribution` | P&L attribution per regime, per strategy |

## How it works

Each agent is a specialized Claude Code subagent with its own system prompt and skill files. The `trading-architect` orchestrates them based on what the current task requires — nightly analysis, trade review, or parameter optimization.

Agents communicate via shared memory files in `/memory/` and skill files in `/skills/`. The guardian agent reads trade outcomes and writes learnings back — closing the feedback loop.

## What's not here

The full system prompts, strategy parameters, and learned skill files are reserved for members.

→ [Join the waitlist at regimelab.dev](https://regimelab.dev)
