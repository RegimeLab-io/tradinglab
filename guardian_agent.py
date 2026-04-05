"""
RegimeLab — Guardian Agent
Monitors bot behavior, identifies losing patterns, and writes learnings
back to skill files to close the feedback loop.
Full implementation available to members at regimelab.dev
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path


logger = logging.getLogger(__name__)


class PatternType(Enum):
    CHASING_MOMENTUM  = "CHASING_MOMENTUM"
    TICKER_BIAS       = "TICKER_BIAS"
    HOUR_WEAKNESS     = "HOUR_WEAKNESS"
    REGIME_MISMATCH   = "REGIME_MISMATCH"
    EARNINGS_OVERLAP  = "EARNINGS_OVERLAP"
    OVERSIZE_POSITION = "OVERSIZE_POSITION"


@dataclass
class LearningPattern:
    pattern_type: PatternType
    description: str
    loss_count: int
    avg_loss_pct: float
    first_seen: datetime
    last_seen: datetime
    active: bool = True


@dataclass
class GuardianReport:
    timestamp: datetime
    trades_analyzed: int
    patterns_found: list[LearningPattern]
    skill_files_updated: list[str]
    blocked_entries_today: int
    regime: str
    recommendations: list[str] = field(default_factory=list)


class GuardianAgent:
    """
    The Guardian Agent closes the learning feedback loop.

    Every night it:
        1. Reads all trades from the past period
        2. Identifies losing patterns (momentum chasing, ticker bias, etc.)
        3. Writes learnings back to skill files
        4. Updates the decision engine's entry filters
        5. Reports what changed and why

    The bot learns from its own mistakes — automatically.
    """

    MIN_LOSSES_TO_BLOCK  = 3
    MIN_LOSS_PCT         = -1.5
    LOOKBACK_DAYS        = 30
    SKILL_FILES_PATH     = Path(".claude/skills")

    def __init__(self, db_connection, skill_path: Path = None):
        self.db = db_connection
        self.skill_path = skill_path or self.SKILL_FILES_PATH
        self.patterns: list[LearningPattern] = []

    def run(self, regime: str) -> GuardianReport:
        """
        Run the full guardian analysis cycle.

        Args:
            regime: Current market regime (BULL/NEUTRAL/BEAR/TURBULENT)

        Returns:
            GuardianReport with all findings and actions taken
        """
        logger.info(f"Guardian agent starting — regime: {regime}")

        trades = self._load_recent_trades()
        patterns = self._detect_patterns(trades, regime)
        updated_files = self._write_skill_files(patterns)
        blocked = self._count_blocked_entries()
        recommendations = self._generate_recommendations(patterns, regime)

        report = GuardianReport(
            timestamp=datetime.now(),
            trades_analyzed=len(trades),
            patterns_found=patterns,
            skill_files_updated=updated_files,
            blocked_entries_today=blocked,
            regime=regime,
            recommendations=recommendations,
        )

        self._log_report(report)
        return report

    def _load_recent_trades(self) -> list[dict]:
        """Load trades from the past LOOKBACK_DAYS days."""
        # Full DB query implementation available to members
        cutoff = datetime.now() - timedelta(days=self.LOOKBACK_DAYS)
        logger.debug(f"Loading trades since {cutoff.date()}")
        return []

    def _detect_patterns(self, trades: list[dict], regime: str) -> list[LearningPattern]:
        """Detect losing patterns in recent trades."""
        patterns = []

        patterns += self._check_momentum_chasing(trades)
        patterns += self._check_ticker_bias(trades)
        patterns += self._check_hour_weakness(trades)
        patterns += self._check_regime_mismatch(trades, regime)

        active = [p for p in patterns if p.active]
        logger.info(f"Detected {len(active)} active patterns")
        return patterns

    def _check_momentum_chasing(self, trades: list[dict]) -> list[LearningPattern]:
        """Detect entries made after large gap-ups (chasing momentum)."""
        # Full implementation available to members
        return []

    def _check_ticker_bias(self, trades: list[dict]) -> list[LearningPattern]:
        """Detect tickers with consistent losses."""
        # Full implementation available to members
        return []

    def _check_hour_weakness(self, trades: list[dict]) -> list[LearningPattern]:
        """Detect hours of day with consistent underperformance."""
        # Full implementation available to members
        return []

    def _check_regime_mismatch(self, trades: list[dict], regime: str) -> list[LearningPattern]:
        """Detect trades entered with wrong regime parameters."""
        # Full implementation available to members
        return []

    def _write_skill_files(self, patterns: list[LearningPattern]) -> list[str]:
        """Write active patterns to Claude Code skill files."""
        updated = []

        for pattern in patterns:
            if not pattern.active:
                continue

            skill_file = self.skill_path / f"{pattern.pattern_type.value.lower()}.md"
            content = self._format_skill_file(pattern)

            self.skill_path.mkdir(parents=True, exist_ok=True)
            skill_file.write_text(content)
            updated.append(str(skill_file))
            logger.info(f"Updated skill file: {skill_file.name}")

        return updated

    def _format_skill_file(self, pattern: LearningPattern) -> str:
        """Format a pattern as a Claude Code skill file."""
        return f"""# {pattern.pattern_type.value}

## Pattern
{pattern.description}

## Stats
- Loss count: {pattern.loss_count} trades
- Avg loss: {pattern.avg_loss_pct:.1f}%
- First seen: {pattern.first_seen.date()}
- Last seen: {pattern.last_seen.date()}

## Action
BLOCK this pattern in entry decisions until further notice.
"""

    def _count_blocked_entries(self) -> int:
        """Count how many entries were blocked today by learned filters."""
        # Full implementation available to members
        return 0

    def _generate_recommendations(
        self, patterns: list[LearningPattern], regime: str
    ) -> list[str]:
        """Generate actionable recommendations based on patterns."""
        recommendations = []

        if any(p.pattern_type == PatternType.CHASING_MOMENTUM for p in patterns if p.active):
            recommendations.append("Reduce gap filter threshold — momentum chasing detected")

        if any(p.pattern_type == PatternType.HOUR_WEAKNESS for p in patterns if p.active):
            recommendations.append("Review entry hour filters — consistent weakness detected")

        if regime == "TURBULENT":
            recommendations.append("TURBULENT regime — consider reducing position sizes")

        return recommendations

    def _log_report(self, report: GuardianReport) -> None:
        """Log guardian report summary."""
        logger.info(
            f"Guardian complete — "
            f"{report.trades_analyzed} trades analyzed, "
            f"{len(report.patterns_found)} patterns found, "
            f"{len(report.skill_files_updated)} skill files updated"
        )


# ── Example usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("RegimeLab Guardian Agent")
    print("→ Join the waitlist at regimelab.dev")
