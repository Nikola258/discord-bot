
def _width(landmarks: list, left: int, right: int) -> float:
    """Calculate horizontal distance between two landmarks"""
    return abs(landmarks[left].x - landmarks[right].x)


def classify_face_shape(landmarks: list) -> str:
    """
    Estimate face shape from MediaPipe Face Landmarker landmarks.

    Returns one of: oval, round, square, triangle, oblong, rectangle

    Uses length_ratio (height/cheekbone) as the main driver:
      < 0.90  = round (very wide/short face)
      0.90-1.40 = oval range (normal face)
      > 1.40  = oblong/rectangle (very long face)

    jaw_forehead_ratio only used as triangle signal when clearly narrow (< 0.78)
    """
    if landmarks is None or len(landmarks) < 455:
        raise ValueError("Insufficient facial landmarks.")

    face_height = abs(landmarks[10].y - landmarks[152].y)
    forehead_width = _width(landmarks, 127, 356)
    cheekbone_width = _width(landmarks, 234, 454)
    jaw_width = _width(landmarks, 172, 397)

    if min(face_height, forehead_width, cheekbone_width, jaw_width) <= 0:
        raise ValueError("Invalid facial landmark measurements.")

    width_to_height = cheekbone_width / face_height
    length_ratio = face_height / cheekbone_width
    jaw_forehead_ratio = jaw_width / forehead_width
    jaw_cheek_ratio = jaw_width / cheekbone_width

    # Very wide face = round
    if width_to_height >= 0.88:
        return "round"

    # Very long face = oblong or rectangle
    if length_ratio > 1.40:
        if jaw_cheek_ratio >= 0.88:
            return "rectangle"
        return "oblong"

    # Normal range (0.90 - 1.40): oval, square, or triangle
    # Only call triangle if jaw is significantly narrower than forehead
    if jaw_forehead_ratio < 0.78:
        return "triangle"

    if jaw_cheek_ratio >= 0.92:
        return "square"

    return "oval"


def calculate_fat_score(landmarks: list) -> int:
    """
    Calculate a fat score (0-100) based on face proportions.

    Calibrated from real faces:
      - Slim face (width_to_height ~0.57) → ~25 (feather)
      - Chubby face (width_to_height ~0.90) → ~75 (chunky)
      - Fatass face (width_to_height ~0.98) → ~94 (fatass)
    """
    if landmarks is None or len(landmarks) < 455:
        raise ValueError("Insufficient facial landmarks.")

    face_height = abs(landmarks[10].y - landmarks[152].y)
    cheekbone_width = _width(landmarks, 234, 454)
    jaw_width = _width(landmarks, 172, 397)

    if face_height <= 0 or cheekbone_width <= 0:
        raise ValueError("Invalid facial landmark measurements.")

    width_to_height = cheekbone_width / face_height
    jaw_fullness = jaw_width / cheekbone_width

    # jaw_fullness is the most reliable fat indicator across all face types.
    # width_to_height is too dependent on camera distance so we drop it.
    # Calibrated from real faces:
    #   0.765 = skeleton (stick)
    #   0.799 = slim (feather ~25)
    #   0.811 = slightly chubby (fat ~55)
    #   0.814 = chubby (chunky ~75)
    #   0.864 = fatass (~94)
    score = (jaw_fullness - 0.75) / (0.87 - 0.75) * 100
    return max(0, min(100, round(score)))


def get_fat_level(score: int) -> str:
    """Return the fun fat-level label for a given score."""
    if score < 17:
        return "stick"
    elif score < 34:
        return "feather"
    elif score < 50:
        return "skinny"
    elif score < 70:
        return "fat"
    elif score < 90:
        return "chunky"
    else:
        return "fatass"
