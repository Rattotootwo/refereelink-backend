"""Tests for FoulDetector cooldown and confidence filtering."""

from __future__ import annotations

import sys
import types
from unittest.mock import MagicMock

import numpy as np


# ---------------------------------------------------------------------------
# The detector module imports `offside.foul_model` at module level, but that
# package is an optional external dependency (fouls_far). Inject a fake module
# before importing FoulDetector so the tests run without real model weights.
# ---------------------------------------------------------------------------
if "offside.foul_model" not in sys.modules:
    fake_offside = types.ModuleType("offside")
    fake_foul_model = types.ModuleType("offside.foul_model")

    class _FakePrediction:
        def __init__(self, confidence: float = 0.0) -> None:
            self.confidence = confidence

    def _fake_load_mvfoul_model(*_args, **_kwargs):
        return MagicMock()

    def _fake_predict_foul_from_frames(*_args, **_kwargs):
        return _FakePrediction(confidence=0.9)

    fake_foul_model.FoulPrediction = _FakePrediction
    fake_foul_model.load_mvfoul_model = _fake_load_mvfoul_model
    fake_foul_model.predict_foul_from_frames = _fake_predict_foul_from_frames
    fake_offside.foul_model = fake_foul_model
    sys.modules["offside"] = fake_offside
    sys.modules["offside.foul_model"] = fake_foul_model

from app.foul_detection.detector import FoulDetector  # noqa: E402


def _make_detector(cooldown_frames: int = 25, confidence: float = 0.5) -> FoulDetector:
    detector = FoulDetector(
        checkpoint_path="dummy.pth",
        device="cpu",
        cooldown_frames=cooldown_frames,
        confidence_threshold=confidence,
    )
    detector._model = MagicMock()
    return detector


def test_drops_noise_on_ten_second_clip():
    """10 秒片段（300 帧）不应产生数百个候选。"""
    detector = _make_detector(cooldown_frames=25)
    detector._latest_prediction = MagicMock(confidence=0.9)

    candidates = [
        detector.update(np.zeros((720, 1280, 3), dtype=np.uint8), frame_index=i) for i in range(300)
    ]

    accepted = [c for c in candidates if c is not None]
    assert len(accepted) < 15, f"Produced too many detections: {len(accepted)}"


def test_avoids_zero_detections_on_foul_clip():
    """代表性犯规片段至少产生 1 个候选。"""
    detector = _make_detector(cooldown_frames=10)
    detector._latest_prediction = MagicMock(confidence=0.85)

    candidates = [
        detector.update(np.zeros((720, 1280, 3), dtype=np.uint8), frame_index=i) for i in range(30)
    ]

    accepted = [c for c in candidates if c is not None]
    assert len(accepted) >= 1, "Produced zero detections on foul clip"


def test_confidence_threshold_filters_weak_predictions():
    """低于置信度阈值的预测应被丢弃。"""
    detector = _make_detector(confidence=0.7)
    detector._latest_prediction = MagicMock(confidence=0.3)

    result = detector.update(np.zeros((720, 1280, 3), dtype=np.uint8), frame_index=100)
    assert result is None
