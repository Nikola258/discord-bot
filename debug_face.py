"""
Run this with a real photo to see the raw landmark measurements.
Usage: python debug_face.py path/to/photo.jpg
"""

import sys
from vision.image_processing import load_image
from vision.face_detection import FaceDetector
from vision.face_classifier import _width

if len(sys.argv) < 2:
    print("Usage: python debug_face.py path/to/photo.jpg")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    image_bytes = f.read()

image_rgb = load_image(image_bytes)

detector = FaceDetector()
faces = detector.detect(image_rgb)
detector.close()

if not faces:
    print("No face detected.")
    sys.exit(1)

landmarks = faces[0]

face_height      = abs(landmarks[10].y - landmarks[152].y)
cheekbone_width  = _width(landmarks, 234, 454)
jaw_width        = _width(landmarks, 172, 397)
forehead_width   = _width(landmarks, 127, 356)

width_to_height  = cheekbone_width / face_height
jaw_fullness     = jaw_width / cheekbone_width
length_ratio     = face_height / cheekbone_width
jaw_forehead     = jaw_width / forehead_width
jaw_cheek        = jaw_width / cheekbone_width

print(f"face_height:     {face_height:.4f}")
print(f"cheekbone_width: {cheekbone_width:.4f}")
print(f"jaw_width:       {jaw_width:.4f}")
print(f"forehead_width:  {forehead_width:.4f}")
print()
print(f"width_to_height: {width_to_height:.4f}  (wider = rounder)")
print(f"jaw_fullness:    {jaw_fullness:.4f}")
print(f"length_ratio:    {length_ratio:.4f}  (taller = slimmer)")
print(f"jaw_forehead:    {jaw_forehead:.4f}")
print(f"jaw_cheek:       {jaw_cheek:.4f}")
