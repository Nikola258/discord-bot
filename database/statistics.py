import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "statistics.json")


def load() -> dict:
    """Load the full statistics database from disk."""
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save(data: dict) -> None:
    """Write the full statistics database back to disk."""
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_user(user_id: str) -> dict | None:
    """Return the stats entry for a user, or None if they don't exist yet."""
    data = load()
    return data.get(str(user_id))


def update_user(user_id: str, updates: dict) -> dict:
    """
    Merge `updates` into the user's stats entry and persist to disk.
    Creates the entry if it doesn't exist yet.
    Returns the updated entry.
    save new info for a user (creates them if they don't exist yet)
    """
    data = load()
    user_id = str(user_id)

    if user_id not in data:
        data[user_id] = {}

    data[user_id].update(updates)
    save(data)
    return data[user_id]


def delete_user(user_id: str) -> bool:
    """Remove a user's entry from the database. Returns True if it existed."""
    data = load()
    user_id = str(user_id)

    if user_id in data:
        del data[user_id]
        save(data)
        return True

    return False
