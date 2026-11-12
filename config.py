
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing {name}. Add it to the .env file in the project folder."
        )
    return value


def get_positive_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, str(default)).strip()

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a whole number.") from exc

    if value <= 0:
        raise RuntimeError(f"{name} must be greater than zero.")

    return value


DISCORD_TOKEN = get_required_env("DISCORD_TOKEN")
FAT_CHECK_CHANNEL_ID = get_positive_int("FAT_CHECK_CHANNEL_ID", 0)
MAX_IMAGE_SIZE_MB = get_positive_int("MAX_IMAGE_SIZE_MB", 8)

MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}
