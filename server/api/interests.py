import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import json
from api.db_functions import get_db
from models import Organization


def populate_interests():
    # print("Populating interests...")
    orgs_path = os.path.join(os.path.dirname(__file__), "interests.json")
    with open(orgs_path, "r") as f:
        orgs = [Organization(**item) for item in json.load(f)]

    conn = get_db()
    cursor = conn.cursor()

    for org in orgs:
        if not org.name.startswith("zzz"):
            cursor.execute(
                "INSERT OR IGNORE INTO interests (name, formatted_name, type, groups) VALUES (?, ?, ?, ?)",
                (org.name, org.formatted_name, "organization", json.dumps(org.groups)),
            )

    conn.commit()
    conn.close()
    print(f"Populated {len(orgs)} interests.")


if __name__ == "__main__":
    populate_interests()
