"""
RegimeLab — Regime Detector
Classifies current market conditions into BULL, NEUTRAL, BEAR, or TURBULENT.
Full implementation available to members at regimelab.dev
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from enum import Enum


class Regime(Enum):
    BULL = "BULL"
    NEUTRAL = "NEUTRAL"
    BEAR = "BEAR"
    TURBULENT = "TURBULENT"


@dataclass
class RegimeSignal:
    regime: Regime
    confidence: float
    spy_vs_ema: float
    vix_level: float
    timestamp: pd.Timestamp


class RegimeDetector:
    """
    Detects market regime using SPY EMA26w and VIX.

    Regimes:
        BULL       — SPY above EMA26w, VIX < 20
        NEUTRAL    — SPY near EMA26w, VIX 20-30
        BEAR       — SPY below EMA26w, VIX > 30
        TURBULENT  — VIX spike > 35, uses BEAR parameters

    Each regime has separately optimized Optuna parameters.
    The bot switches parameters automatically when regime changes.
    """

    BULL_VIX_THRESHOLD = 20.0
    BEAR_VIX_THRESHOLD = 30.0
    TURBULENT_VIX_THRESHOLD = 35.0
    EMA_WEEKS = 26
    NEUTRAL_BAND = 0.02  # 2% band around EMA

    def __init__(self, spy_data: pd.DataFrame, vix_data: pd.DataFrame):
        self.spy = spy_data
        self.vix = vix_data
        self._ema = self._calculate_ema()

    def _calculate_ema(self) -> pd.Series:
        """Calculate SPY EMA over 26 weeks."""
        weekly = self.spy["close"].resample("W").last()
        return weekly.ewm(span=self.EMA_WEEKS, adjust=False).mean()

    def detect(self, timestamp: pd.Timestamp = None) -> RegimeSignal:
        """
        Detect current market regime.

        Returns:
            RegimeSignal with regime, confidence, and raw signals
        """
        if timestamp is None:
            timestamp = pd.Timestamp.now()

        spy_price = self._get_spy_price(timestamp)
        vix_level = self._get_vix_level(timestamp)
        ema_value = self._get_ema_value(timestamp)

        spy_vs_ema = (spy_price - ema_value) / ema_value
        regime, confidence = self._classify(spy_vs_ema, vix_level)

        return RegimeSignal(
            regime=regime,
            confidence=confidence,
            spy_vs_ema=round(spy_vs_ema, 4),
            vix_level=round(vix_level, 2),
            timestamp=timestamp,
        )

    def _classify(self, spy_vs_ema: float, vix: float) -> tuple[Regime, float]:
        """Classify regime based on SPY vs EMA and VIX level."""

        # Turbulent overrides everything
        if vix >= self.TURBULENT_VIX_THRESHOLD:
            confidence = min(1.0, (vix - self.TURBULENT_VIX_THRESHOLD) / 10)
            return Regime.TURBULENT, round(confidence, 2)

        # Bear: below EMA and high VIX
        if spy_vs_ema < -self.NEUTRAL_BAND and vix >= self.BEAR_VIX_THRESHOLD:
            confidence = min(1.0, abs(spy_vs_ema) * 10 + (vix - 30) / 20)
            return Regime.BEAR, round(confidence, 2)

        # Bull: above EMA and low VIX
        if spy_vs_ema > self.NEUTRAL_BAND and vix < self.BULL_VIX_THRESHOLD:
            confidence = min(1.0, spy_vs_ema * 10 + (20 - vix) / 20)
            return Regime.BULL, round(confidence, 2)

        # Neutral: everything in between
        confidence = 1.0 - min(1.0, abs(spy_vs_ema) * 5 + abs(vix - 25) / 25)
        return Regime.NEUTRAL, round(max(0.1, confidence), 2)

    def _get_spy_price(self, timestamp: pd.Timestamp) -> float:
        """Get SPY closing price at or before timestamp."""
        return float(self.spy["close"].asof(timestamp))

    def _get_vix_level(self, timestamp: pd.Timestamp) -> float:
        """Get VIX level at or before timestamp."""
        return float(self.vix["close"].asof(timestamp))

    def _get_ema_value(self, timestamp: pd.Timestamp) -> float:
        """Get EMA value at or before timestamp."""
        return float(self._ema.asof(timestamp))


# ── Example usage ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # This is a simplified example.
    # Full implementation with live IBKR data feed available to members.
    print("RegimeLab Regime Detector")
    print("→ Join the waitlist at regimelab.dev")
