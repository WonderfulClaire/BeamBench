"""Small signal-preparation helpers often repeated in audio experiments."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def rms_normalize(signal: ArrayLike, target_dbfs: float = -20.0) -> NDArray[np.float64]:
    """Scale a signal to the requested RMS level without changing its shape."""
    array = np.asarray(signal, dtype=float)
    rms = float(np.sqrt(np.mean(np.square(array))))
    if rms < np.finfo(float).eps:
        return array.copy()
    target = 10.0 ** (target_dbfs / 20.0)
    return array * (target / rms)


def trim_silence(signal: ArrayLike, threshold_db: float = -45.0) -> NDArray[np.float64]:
    """Trim leading and trailing samples below a peak-relative threshold."""
    array = np.asarray(signal, dtype=float)
    if array.ndim != 1:
        raise ValueError("trim_silence expects a one-dimensional signal")
    peak = float(np.max(np.abs(array), initial=0.0))
    if peak == 0.0:
        return array[:0].copy()
    active = np.flatnonzero(np.abs(array) >= peak * 10.0 ** (threshold_db / 20.0))
    if active.size == 0:
        return array[:0].copy()
    return array[active[0] : active[-1] + 1].copy()


def frame_signal(
    signal: ArrayLike,
    frame_length: int,
    hop_length: int,
    *,
    pad: bool = False,
) -> NDArray[np.float64]:
    """Create overlapping frames with a predictable ``(frames, samples)`` shape."""
    array = np.asarray(signal, dtype=float)
    if array.ndim != 1:
        raise ValueError("frame_signal expects a one-dimensional signal")
    if frame_length <= 0 or hop_length <= 0:
        raise ValueError("frame_length and hop_length must be positive")
    if pad and (array.size < frame_length or (array.size - frame_length) % hop_length):
        needed = max(
            frame_length,
            frame_length
            + int(np.ceil(max(0, array.size - frame_length) / hop_length)) * hop_length,
        )
        array = np.pad(array, (0, needed - array.size))
    if array.size < frame_length:
        return np.empty((0, frame_length), dtype=float)
    count = 1 + (array.size - frame_length) // hop_length
    starts = np.arange(count)[:, None] * hop_length
    offsets = np.arange(frame_length)[None, :]
    return array[starts + offsets].copy()
