
from pathlib import Path

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import numpy as np


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "face_landmarker.task"
)


class FaceDetector:
    """Detect faces and extract facial landmarks using MediaPipe"""

    def __init__(self, model_path: Path = MODEL_PATH):
        model_path = Path(model_path)

        if not model_path.is_file() or model_path.stat().st_size == 0:
            raise FileNotFoundError(
                f"Face Landmarker model is missing or empty: {model_path}"
            )

        options = vision.FaceLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path=str(model_path)
            ),
            running_mode=vision.RunningMode.IMAGE,
            num_faces=5,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self._detector = vision.FaceLandmarker.create_from_options(
            options
        )

    def detect(self, image_rgb: np.ndarray) -> list:
        """
        Detect faces in an RGB image

        Returns a list containing one landmark list per detected face
        """
        if not isinstance(image_rgb, np.ndarray):
            raise TypeError("image_rgb must be a NumPy array.")

        if (
            image_rgb.ndim != 3
            or image_rgb.shape[2] != 3
            or image_rgb.dtype != np.uint8
        ):
            raise ValueError(
                "Expected an RGB image with three uint8 channels."
            )

        image_rgb = np.ascontiguousarray(image_rgb)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=image_rgb,
        )

        result = self._detector.detect(mp_image)

        return result.face_landmarks

    def close(self) -> None:
        """Release MediaPipe resources"""
        self._detector.close()
