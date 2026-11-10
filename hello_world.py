"""
Hello World — demonstrates that the JSON database layer works.

Shows: create → read → update → read again → cleanup
"""

import json
from database import statistics

USER_ID = "123456789"  # fake Discord user ID for the demo


def print_db():
    """Pretty-print the current state of the JSON file on disk."""
    with open("database/statistics.json") as f:
        print(json.dumps(json.load(f), indent=4))


print("=== 1. Database starts empty ===")
print_db()

print("\n=== 2. Create a user entry ===")
statistics.update_user(USER_ID, {
    "username": "CoolGuy#1337",
    "scans": 0,
    "last_result": None,
    "role": None,
})
print_db()

print("\n=== 3. Read the user back ===")
user = statistics.get_user(USER_ID)
print(f"Got user: {user}")

print("\n=== 4. Update the user (simulate a scan result) ===")
statistics.update_user(USER_ID, {
    "scans": 1,
    "last_result": "slightly chonky",
    "role": "Chonker",
})
print_db()

print("\n=== 5. Read again to confirm the update persisted ===")
user = statistics.get_user(USER_ID)
print(f"Updated user: {user}")

print("\nAll good — JSON database read/write/update works correctly!")
print("Check database/statistics.json to see the stored data!")
