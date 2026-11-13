## Testing commands

Here live all the commands used for testing

### Testing commands for vision

```cmd - commands

// Test if facial landmarks detection work

python -c "from PIL import Image; import numpy as np; from vision.image_processing import load_image; from vision.face_detection import FaceDetector; from vision.face_classifier import classify_face_shape; img=load_image(open('test_face.jpg','rb').read()); d=FaceDetector(); faces=d.detect(img); print('Faces detected:',len(faces)); print('Face shapes:',[classify_face_shape(f) for f in faces]); d.close()"

// Pillow can decode an image

python -c "from io import BytesIO; from PIL import Image; from vision.image_processing import load_image; b=BytesIO(); Image.new('RGB',(64,64),'white').save(b,format='PNG'); a=load_image(b.getvalue()); print('Image:', a.shape, a.dtype)"

// MediaPipe can load the model and detect faces

python -c "import numpy as np; from vision.face_detection import FaceDetector; d=FaceDetector(); print('Model loaded successfully'); print('Faces in blank image:', len(d.detect(np.zeros((256,256,3), dtype=np.uint8)))); d.close()"

// Check if the classifier works

python -c "from vision.face_classifier import classify_face_shape; print('Classifier imported successfully')"

```

## Automated testing (planned)

Currently, the vision components are tested manually using Python commands. In the future, these manual tests should be replaced with automated tests using **pytest**.

The automated tests should be stored here:

```text
tests/
├── test_image_processing.py
├── test_face_detection.py
└── test_statistics.py
```

**Planned test files:**

| File | Responsibility |
|---|---|
| `test_image_processing.py` | Tests image loading, decoding, resizing, and invalid image handling |
| `test_face_detection.py` | Tests MediaPipe model initialization, facial landmark detection, and handling images without faces |
| `test_statistics.py` | Tests saving, loading, and updating anonymous statistics in the JSON file |

The tests should use `pytest` and, where possible, sample images or mock objects instead of requiring a live Discord connection.

In the future, these tests could also be executed automatically using GitHub Actions whenever new code is pushed to the repository or a pull request is created.