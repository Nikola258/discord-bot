
def _width(landmarks: list, left: int, right: int) -> float:
    """Calculate horizontal distance between two landmarks"""
    return abs(landmarks[left].x - landmarks[right].x)


def classify_face_shape(landmarks: list) -> str:
    """
    Estimate face shape from MediaPipe Face Landmarker landmarks

    Returns one of:
    oval, round, square, triangle, oblong, rectangle

    This is a rough geometric heuristic, not a definitive assessment
    """

    if landmarks is None or len(landmarks) < 455:
        raise ValueError("Insufficient facial landmarks.")

    # Vertical distance from forehead to chin
    face_height = abs(landmarks[10].y - landmarks[152].y)

    # Horizontal facial measurements
    forehead_width = _width(landmarks, 127, 356)
    cheekbone_width = _width(landmarks, 234, 454)
    jaw_width = _width(landmarks, 172, 397)

    if min(face_height, forehead_width, cheekbone_width, jaw_width) <= 0:
        raise ValueError("Invalid facial landmark measurements.")

    length_ratio = face_height / cheekbone_width
    jaw_forehead_ratio = jaw_width / forehead_width
    jaw_cheek_ratio = jaw_width / cheekbone_width

    # Wider jaw compared with forehead
    if jaw_forehead_ratio > 1.12:
        return "triangle"

    # Shorter, fuller-looking face proportions
    if length_ratio < 1.25:
        return "round"

    # Longer face with a relatively narrow jaw
    if length_ratio >= 1.55:
        if jaw_cheek_ratio >= 0.85:
            return "rectangle"
        return "oblong"

    # Strong jaw and relatively similar facial widths
    if length_ratio < 1.38 and jaw_cheek_ratio >= 0.88:
        return "square"

    return "oval"
