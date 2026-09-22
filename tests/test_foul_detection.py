"""Tests for FoulDetector cooldown and confidence filtering."""

from __future__ import annotations

import sys
import types
from unittest.mock import MagicMock, patch

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

    fake_foul_model.FoulPrediction = _FakePrediction
    fake_foul_model.load_mvfoul_model = lambda *a, **k: MagicMock()
    fake_foul_model.predict_foul_from_frames = lambda *a, **k: _FakePrediction(0.9)
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


@patch("app.foul_detection.detector.predict_foul_from_frames")
def test_drops_noise_on_ten_second_clip(mock_predict):
    """300 帧输入 -> 候选数 < 15，且推理确实被执行。"""
    mock_predict.return_value = MagicMock(confidence=0.9)
    detector = _make_detector(cooldown_frames=25)

    candidates = [
        detector.update(np.zeros((720, 1280, 3), dtype=np.uint8), frame_index=i) for i in range(300)
    ]

    accepted = [c for c in candidates if c is not None]
    assert len(accepted) < 15
    assert mock_predict.call_count > 0


@patch("app.foul_detection.detector.predict_foul_from_frames")
def test_avoids_zero_detections_on_foul_clip(mock_predict):
    """犯规片段至少产生 1 个候选。"""
    mock_predict.return_value = MagicMock(confidence=0.85)
    detector = _make_detector(cooldown_frames=10)

    candidates = [
        detector.update(np.zeros((720, 1280, 3), dtype=np.uint8), frame_index=i) for i in range(30)
    ]

    accepted = [c for c in candidates if c is not None]
    assert len(accepted) >= 1


@patch("app.foul_detection.detector.predict_foul_from_frames")
def test_weak_inference_output_is_filtered(mock_predict):
    """推理生成的低置信度预测会被过滤。"""
    mock_predict.return_value = MagicMock(confidence=0.2)
    detector = _make_detector(confidence=0.7)

    results = [
        detector.update(np.zeros((720, 1280, 3), dtype=np.uint8), frame_index=i) for i in range(50)
    ]
    assert all(r is None for r in results)
    assert mock_predict.call_count > 0
