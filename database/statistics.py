import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "statistics.json")

_EMPTY_DB = {
    "aggregates": {
        "total_scans": 0,
        "average_score": 0.0,
        "face_shape_counts": {
            "oval": 0,
            "round": 0,
            "square": 0,
            "triangle": 0,
            "oblong": 0,
            "rectangle": 0,
        },
        "fat_level_counts": {
            "stick": 0,
            "feather": 0,
            "skinny": 0,
            "fat": 0,
            "chunky": 0,
            "fatass": 0,
        },
    },
    "users": {},
}


def load() -> dict:
    """Load the database from disk. Creates an empty one if missing."""
    if not os.path.exists(DB_PATH):
        save(_EMPTY_DB.copy())
        return _EMPTY_DB.copy()
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save(data: dict) -> None:
    """Write the database to disk."""
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_user(user_id: str) -> dict | None:
    """Return the stored entry for a user, or None if they haven't scanned yet."""
    data = load()
    return data["users"].get(str(user_id))


def record_scan(user_id: str, face_shape: str, score: int, fat_level: str) -> None:
    """
    Record a scan result:
    - Updates the user's personal entry (last result + scan count)
    - Updates server-wide aggregate counts and recalculates average score

    No usernames or photos are stored — only the Discord user ID and results.
    """
    data = load()
    user_id = str(user_id)

    # --- Per-user entry (non-anonymous, used to avoid duplicate aggregate counts) ---
    user = data["users"].get(user_id, {"scans": 0})
    user["scans"] = user.get("scans", 0) + 1
    user["last_shape"] = face_shape
    user["last_score"] = score
    user["last_fat_level"] = fat_level
    data["users"][user_id] = user

    # --- Anonymous aggregates ---
    agg = data["aggregates"]
    agg["total_scans"] += 1

    if face_shape in agg["face_shape_counts"]:
        agg["face_shape_counts"][face_shape] += 1

    if fat_level in agg["fat_level_counts"]:
        agg["fat_level_counts"][fat_level] += 1

    # Recalculate running average score
    prev_avg = agg["average_score"]
    total = agg["total_scans"]
    agg["average_score"] = round(((prev_avg * (total - 1)) + score) / total, 1)

    save(data)


def get_aggregates() -> dict:
    """Return the anonymous server-wide aggregate statistics."""
    return load()["aggregates"]


def delete_user(user_id: str) -> bool:
    """Remove a user's personal entry. Returns True if it existed."""
    data = load()
    user_id = str(user_id)
    if user_id in data["users"]:
        del data["users"][user_id]
        save(data)
        return True
    return False
