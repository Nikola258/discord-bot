
from io import BytesIO
import warnings

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError


MAX_IMAGE_SIZE_BYTES = 8 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


class InvalidImageError(ValueError):
    """Raised when an uploaded image is invalid or unsupported"""


def load_image(image_bytes: bytes) -> np.ndarray:
    """
    Validate image bytes and return an RGB NumPy array

    The returned array has shape (height, width, 3)
    """

    if not isinstance(image_bytes, bytes) or not image_bytes:
        raise InvalidImageError("The uploaded file is empty.")

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise InvalidImageError("The image exceeds the 8 MB size limit.")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)

            # First pass: verify the image file
            with Image.open(BytesIO(image_bytes)) as image:
                if image.format not in ALLOWED_FORMATS:
                    raise InvalidImageError(
                        "Only JPEG, PNG, and WEBP images are supported."
                    )

                if image.width * image.height > MAX_IMAGE_PIXELS:
                    raise InvalidImageError(
                        "The image dimensions are too large."
                    )

                image.verify()

            # Second pass: decode the verified image
            with Image.open(BytesIO(image_bytes)) as image:
                image = ImageOps.exif_transpose(image)
                image = image.convert("RGB")

                if image.width * image.height > MAX_IMAGE_PIXELS:
                    raise InvalidImageError(
                        "The image dimensions are too large."
                    )

                return np.asarray(image, dtype=np.uint8).copy()

    except InvalidImageError:
        raise

    except (
        UnidentifiedImageError,
        OSError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
        ValueError,
    ) as exc:
        raise InvalidImageError(
            "The uploaded file is not a valid image."
        ) from exc
