import sys
import os
from typing import Any

# Allow this module to import server-level files like models.py when it is run
# from inside server/ or imported through the test target.
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import json
import unicodedata

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from api.sql_init import initialize_database
from api.db_functions import get_db
from models import Organization

# Source context used while developing the scraper:
# - https://realpython.com/beautiful-soup-web-scraper-python/
# - https://scrapfly.io/blog/posts/web-scraping-with-playwright-and-python
# - https://github.com/seehorne/GetGrinnected

JSON_URL = "https://events.grinnell.edu/live/json/events/response_fields/all/paginate"

# Load organization metadata once. The scraper uses this to link events to
# matching interests after inserting events into the database.
with open("api/interests.json", "r") as file:
    data = json.load(file)
    data = [Organization(**item) for item in data]
    INTERESTS = {item.name: item for item in data}
    INTERESTS_COMMA = [item for item in data if item.has_comma]

# Purpose: Clean plain text fields returned by LiveWhale.
# Input: text, which may be a string or None.
# Output: A string with repeated whitespace removed, or "" for missing text.
def clean_text(text: str | None) -> str:
    """Remove repeated whitespace from text returned by LiveWhale."""
    if text is None:
        return ""
    return " ".join(str(text).split())

# Purpose: Convert HTML snippets from LiveWhale into readable plain text.
# Input: html_text, which may be an HTML string or None.
# Output: Plain text with tags removed, or "" for missing HTML.
def clean_html(html_text: str | None) -> str:
    """Remove HTML tags from JSON fields like summary and description."""
    if html_text is None:
        return ""

    soup = BeautifulSoup(html_text, "html.parser")
    return clean_text(soup.get_text(" "))

# Purpose: Request one page of event data from the LiveWhale JSON API.
# Input: page_num, the page number to fetch.
# Output: The decoded JSON response for that page.
def get_json_page(page_num: int) -> Any:
    """Fetch one paginated JSON response from the LiveWhale events API."""
    url = JSON_URL + "?page=" + str(page_num)
    return requests.get(url).json()

# Purpose: Normalize organization names before matching them to interests.
# Input: s, an organization name string from LiveWhale or interests data.
# Output: Lowercase ASCII text with quotes/accents removed.
def sanitize_name(s: str) -> str:
    """Normalize organization names so they can be matched to interests."""
    s = (
        s.replace("’", "")
        .replace("‘", "")
        .replace("'", "")
        .replace("“", "")
        .replace("”", "")
    )
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s.lower().strip()

# Purpose: Look up an interest row by name.
# Input: cursor, an active SQLite cursor; name, the interest name to find.
# Output: The interest id if found, otherwise None.
def get_interest_id(cursor, name):
    """Return the id for an interest name, or None if it is not in the DB."""
    name = clean_text(name).lower()
    cursor.execute(
        """
        SELECT id FROM interests WHERE LOWER(name) = ?
        """,
        (name,),
    )
    result = cursor.fetchone()
    return result[0] if result else None

# Purpose: Link one scraped event to one interest in the join table.
# Input: cursor, an active SQLite cursor; name, an interest name; event_id, the DB event id.
# Output: None. The database is updated only if the interest name is recognized.
def add_event_interest(cursor, name, event_id):
    """Add the event-interest link if the scraped organization is recognized."""
    interest_id = get_interest_id(cursor, name)
    if not interest_id:
        return

    cursor.execute(
        """
        INSERT OR IGNORE INTO event_interests (event_id, interest_id)
        VALUES (?, ?)
        """,
        (event_id, interest_id),
    )

# Purpose: Find an interest name from a list of interest rows.
# Input: interest_id, the id to search for; interests, rows shaped like (id, name, ...).
# Output: The matching interest name, or None if no row matches.
def get_interest_by_id(interest_id, interests):
    """Return an interest name from a list of interest rows."""
    for interest in interests:
        if interest[0] == interest_id:
            return interest[1]
    return None

# Purpose: Scrape LiveWhale events, store them in SQLite, and return parsed data.
# Input: None. Reads from the LiveWhale API and the configured SQLite database.
# Output: A dictionary of scraped events keyed by local integer ids.
def scrape_events():
    """Scrape LiveWhale events, save them to SQLite, and return event data."""
    print("Scraping LiveWhale events...")
    initialize_database()

    connection = get_db()
    cursor = connection.cursor()

    # Rebuild event_interests after events are recreated.
    cursor.execute("PRAGMA foreign_keys = OFF")
    cursor.execute("DROP TABLE IF EXISTS event_interests")
    cursor.execute("PRAGMA foreign_keys = ON")

    events = {}
    inserted_count = 0

    # The first page tells us how many pages LiveWhale currently has.
    first_page = get_json_page(1)
    total_pages = first_page["meta"]["total_pages"]

    # Go through every page and insert each raw LiveWhale event into the DB.
    for i in range(1, total_pages + 1):
        page_json = get_json_page(i)
        raw_events = page_json.get("data", [])

        for event in raw_events:
            # Required and optional event fields from LiveWhale.
            id = clean_text(event.get("id"))
            title = clean_text(event.get("title"))
            start_time = clean_text(event.get("date_iso"))

            # Some LiveWhale events do not list an end time. Store an empty
            # string instead of crashing on an undefined variable.
            end_time = ""
            if event.get("date2_time"):
                end_time = clean_text(event.get("date2_iso"))

            location = clean_text(event.get("location"))

            # Summary is usually the useful description, but some events may
            # only provide description.
            summary = clean_html(event.get("summary"))
            if not summary:
                summary = clean_html(event.get("description"))

            categories = ""
            if event.get("event_types"):
                categories = ",".join(event.get("event_types"))

            tags = ""
            if event.get("tags"):
                tags = ",".join(event.get("tags"))

            org_name = ""
            if event.get("custom_organization"):
                org_name = clean_text(event.get("custom_organization"))

            # Keep the same dictionary shape the rest of the app/tests expect.
            events[inserted_count] = {
                "id": inserted_count,
                "event_id": id,
                "creation_time_stamp": (datetime.now(timezone.utc)).isoformat(),
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
                "summary": summary,
                "categories": categories,
                "tags": tags,
                "org_name": org_name,
                "occurances": None,
            }

            cursor.execute(
                """
                INSERT INTO events (
                    id, event_id, title, creation_time_stamp, start_time, end_time,
                    location, summary, categories, tags, org_name
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    inserted_count,
                    id,
                    title,
                    (datetime.now(timezone.utc)).isoformat(),
                    start_time,
                    end_time,
                    location,
                    summary,
                    categories,
                    tags,
                    org_name,
                ),
            )

            event_id = cursor.lastrowid

            # Link the event to matching interests based on organization name.
            if org_name:
                org_name = sanitize_name(clean_html(org_name))
                interests = org_name.split(", ")

                # Some organization names contain commas, so naive splitting
                # would miss them. Add known comma-containing orgs manually.
                if "," in org_name:
                    interests.extend(
                        interest.name
                        for interest in INTERESTS_COMMA
                        if interest.name in org_name
                    )

                for interest in interests:
                    add_event_interest(cursor, interest, event_id)

            inserted_count += 1

    connection.commit()
    connection.close()

    print("Events count before occurance detection:", len(events))
    occurance_finder(events)
    print("Events count after occurance detection:", len(events))
    print("Inserted " + str(inserted_count) + " events into the database.")

    return events

# Purpose: Detect repeated event titles and combine them as recurring occurrences.
# Input: events, the dictionary returned by scrape_events before recurrence merging.
# Output: None. The events dictionary is mutated in place.
def occurance_finder(events):
    """Combine repeated event titles into one event with an occurances list.

    Only events in the next 30 days are considered recurring. That prevents
    unrelated events far apart in time from being merged just because they have
    the same title.
    """
    now = datetime.now(timezone.utc)
    month_end = now + timedelta(days=30)

    events_within_30days = {}
    for event in events.values():
        if not event.get("start_time"):
            continue

        start_dt = datetime.fromisoformat(event["start_time"])
        if start_dt > month_end:
            continue
        events_within_30days[event["id"]] = event

    frequency_dict = dict()
    for event in events_within_30days.values():
        title = event["title"]
        if title not in frequency_dict:
            frequency_dict[title] = []
        frequency_dict[title].append(event.get("id"))

    for title in frequency_dict:
        if len(frequency_dict[title]) > 1:
            first_id = frequency_dict[title][0]
            events[first_id]["occurances"] = []

            for id in frequency_dict[title]:
                events[first_id]["occurances"].append(
                    {
                        "start": events[id]["start_time"],
                        "end": events[id]["end_time"],
                    }
                )
                if id != first_id:
                    events.pop(id, None)

# Purpose: Print a small sample of stored events for manual inspection/debugging.
# Input: None. Reads from the configured SQLite database.
# Output: None. Prints the first five database event rows.
def test_scraping():
    """Print the first five database events for manual scraper inspection."""
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, event_id, creation_time_stamp, title, start_time, end_time,
            location, summary, categories, tags, org_name, frequency
        FROM events
        LIMIT 5
        """
    )

    db_events = cursor.fetchall()
    connection.close()

    print("\nFirst 5 events in database:")
    for event in db_events:
        print("Unique ID:", event[0])
        print("Event ID:", event[1])
        print("\tCreated:", event[2])
        print("\tTitle:", event[3])
        print("\tStart:", event[4])
        print("\tEnd:", event[5])
        print("\tLocation:", event[6])
        print("\tSummary:", event[7])
        print("\tCategories:", event[8])
        print("\tTags:", event[9])
        print("\tOrg Name:", event[10])
        print("\tFrequency:", event[11])
        print()


if __name__ == "__main__":
    events = scrape_events()
    test_scraping()
    print("Number of events found:", len(events))
