"""Shared progress-reporting utilities used by pipeline stages."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


_LEVEL_ORDER = {"quiet": 0, "normal": 1, "verbose": 2}


def _normalize_level(level: str) -> str:
    return level if level in _LEVEL_ORDER else "normal"


@dataclass(frozen=True)
class StageContext:
    """Identifies a pipeline stage and its position in the current run."""

    name: str
    current: int | None = None
    total: int | None = None


class ProgressReporter:
    """Emit structured, human-readable progress events to stdout."""

    def __init__(self, verbosity: str = "normal", timestamps: bool = True) -> None:
        """Create a console progress reporter with configurable verbosity."""
        self.verbosity = _normalize_level(verbosity)
        self.timestamps = timestamps

    def pipeline_start(self, command: str, total_stages: int) -> None:
        """Emit a pipeline-start event."""
        self.info(
            stage="pipeline",
            progress=f"0/{total_stages}",
            message=f"starting command={command}",
        )

    def pipeline_complete(self, duration_seconds: float) -> None:
        """Emit a pipeline-complete event with elapsed time."""
        self.info(
            stage="pipeline",
            progress="complete",
            message=f"finished in {duration_seconds:.2f}s",
        )

    def pipeline_failed(self, duration_seconds: float, error: Exception) -> None:
        """Emit a pipeline-failed event with elapsed time and exception."""
        self.error(
            stage="pipeline",
            progress="failed",
            message=f"failed after {duration_seconds:.2f}s: {error}",
        )

    def stage_start(self, context: StageContext) -> None:
        """Emit a stage-start event for the provided stage context."""
        progress = self._format_progress(context.current, context.total)
        self.info(stage=context.name, progress=progress, message="started")

    def stage_complete(
        self,
        context: StageContext,
        duration_seconds: float,
        metrics: Mapping[str, object] | None = None,
    ) -> None:
        """Emit a stage-complete event with optional metrics."""
        progress = self._format_progress(context.current, context.total)
        suffix = self._format_metrics(metrics)
        self.info(
            stage=context.name,
            progress=progress,
            message=f"completed in {duration_seconds:.2f}s{suffix}",
        )

    def stage_failed(
        self,
        context: StageContext,
        duration_seconds: float,
        error: Exception,
    ) -> None:
        """Emit a stage-failed event for the provided stage context."""
        progress = self._format_progress(context.current, context.total)
        self.error(
            stage=context.name,
            progress=progress,
            message=f"failed after {duration_seconds:.2f}s: {error}",
        )

    def step(
        self,
        *,
        stage: str,
        message: str,
        current: int | None = None,
        total: int | None = None,
        level: str = "normal",
        metrics: Mapping[str, object] | None = None,
    ) -> None:
        """Emit an ad-hoc progress step for a pipeline stage."""
        progress = self._format_progress(current, total)
        suffix = self._format_metrics(metrics)
        self._emit(
            level=_normalize_level(level),
            stage=stage,
            progress=progress,
            message=f"{message}{suffix}",
        )

    def info(self, *, stage: str, progress: str, message: str) -> None:
        """Emit an informational progress message."""
        self._emit(level="normal", stage=stage, progress=progress, message=message)

    def warning(self, *, stage: str, progress: str, message: str) -> None:
        """Emit a warning progress message."""
        self._emit(level="normal", severity="WARN", stage=stage, progress=progress, message=message)

    def error(self, *, stage: str, progress: str, message: str) -> None:
        """Emit an error progress message."""
        self._emit(level="quiet", severity="ERROR", stage=stage, progress=progress, message=message)

    def _emit(
        self,
        *,
        level: str,
        stage: str,
        progress: str,
        message: str,
        severity: str = "INFO",
    ) -> None:
        if not self._should_emit(level):
            return
        timestamp = datetime.now().strftime("%H:%M:%S") if self.timestamps else "-"
        print(f"{timestamp} | {severity} | {stage} | {progress} | {message}")

    def _should_emit(self, event_level: str) -> bool:
        return _LEVEL_ORDER[event_level] <= _LEVEL_ORDER[self.verbosity]

    @staticmethod
    def _format_progress(current: int | None, total: int | None) -> str:
        if current is None or total is None:
            return "-"
        return f"{current}/{total}"

    @staticmethod
    def _format_metrics(metrics: Mapping[str, object] | None) -> str:
        if not metrics:
            return ""
        pairs = ", ".join(f"{key}={value}" for key, value in metrics.items())
        return f" ({pairs})"
