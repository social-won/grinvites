from pathlib import Path
from typing import Any


import json
import unicodedata

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# from sql_init import initialize_database
from api.db_functions import get_db
from api.sql_init import initialize_database
from models import Organization
from api.interests import populate_interests

# Source: https://realpython.com/beautiful-soup-web-scraper-python/
# Source: https://scrapfly.io/blog/posts/web-scraping-with-playwright-and-python
# Source: https://github.com/seehorne/GetGrinnected
BASE_DIR = Path(__file__).resolve().parent
JSON_URL = "https://events.grinnell.edu/live/json/events/response_fields/all/paginate"
INTEREST_FILE = BASE_DIR / "interests.json"

with open(INTEREST_FILE, "r") as file:
    data = [Organization(**item) for item in json.load(file)]
    INTERESTS = {item.name: item for item in data}
    INTERESTS_COMMA = [item for item in data if item.has_comma]


# Helper function to clean text by removing extra whitespace
def clean_text(text: str | None) -> str:
    """Cleans text by removing extra whitespace.

    Args:
        text (str | None): string to be cleaned

    Returns:
        str: cleaned text
    """
    if text is None:
        return ""
    return " ".join(str(text).split())


def clean_html(html_text: str | None) -> str:
    """Removes HTML tags from JSON fields like summary/description.

    Args:
        html_text (str | None): html text

    Returns:
        str: Plain text html without tags.
    """
    if not html_text:
        return ""

    soup = BeautifulSoup(html_text, "html.parser")
    return clean_text(soup.get_text(" "))


def get_json_page(page_num: int) -> dict[str, Any]:
    """Fetches one JSON page from the JSON_URL endpoint.

    Args:
        page_num (int): page number

    Returns:
        Any: JSON diction of the provided event page.
    """

    url = JSON_URL + "?page=" + str(page_num)
    response = requests.get(url)
    response.raise_for_status()  # raise HTTP error if page is inaccessible
    return response.json()


def sanitize_name(s: str) -> str:
    s = (
        s.replace("’", "")
        .replace("‘", "")
        .replace("'", "")
        .replace("“", "")
        .replace("”", "")
    )
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s.lower().strip()


# adds interest to interest table
# def add_interest(cursor, name, interest_type="organization"):
#     if not name:
#         return
#     name = sanitize_name(clean_html(name))
#     interests = name.split(", ")
#     # corrects for potential incorrect splitting of name by adding in any org with a comma in their name
#     if "," in name:
#         interests.extend(org.name for org in ORGS_COMMA if org.name in name)

#     for interest in interests:
#         try:
#             item = ORGS[interest]
#         # if cursor.execute('''SELECT EXISTS(SELECT 1 FROM interests WHERE name = ?)''', (interest,)):
#             cursor.execute('''
#             INSERT OR IGNORE INTO interests (name, formatted_name, type, groups)
#             VALUES (?, ?, ?, ?)
#             ''', (item.name, item.formatted_name, interest_type, json.dumps(item.groups)))
#         except KeyError:
#             print(interest, "not found")


# gets the id of an interest
def get_interest_id(cursor, name: str) -> int | None:
    """ets the database Id of an interest by its name.


    Args:
        cursor (_type_): _description_
        name (str): _description_

    Returns:
        int | None: _description_
    """

    name = clean_text(name).lower()
    cursor.execute("SELECT id FROM interests WHERE LOWER(name) = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else None


def add_event_interest(cursor, name: str, event_id: str) -> None:
    """Adds event interest to events interest table.

    Args:
        cursor (_type_): _description_
        name (str): _description_
        event_id (str): _description_
    """
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


def get_interest_by_id(interest_id, interests):
    for interest in interests:
        if interest[0] == interest_id:
            return interest[1]
    return None


def scrape_events() -> dict[str, dict]:
    """Scrape events from the LiveWhale JSON endpoint and stores them in the database.

    Returns:
        dict[str, dict]: _description_
    """

    print("scraping events...")
    initialize_database()
    connection = get_db()
    cursor = connection.cursor()

    # Temporarily disable FK constraints for initialization
    cursor.execute("PRAGMA foreign_keys = OFF")
    # cursor.execute("DELETE FROM events")
    # cursor.execute("DELETE FROM interests")
    # cursor.execute("DELETE FROM event_interests")
    cursor.execute("PRAGMA foreign_keys = ON")

    events = {}

    inserted_count = 0

    try:
        # Get first page so we can learn how many total pages exist
        first_page = get_json_page(1)

        # The JSON file includes meta.total_pages, e.g. page 9 of 9 in your pasted file
        total_pages = first_page["meta"]["total_pages"]

        # Go through every page
        for i in range(1, total_pages + 1):
            page_json = get_json_page(i)

            # Each page stores event records inside the "data" list
            raw_events = page_json.get("data", [])

            for event in raw_events:

                # Get id
                event_id = clean_text(event.get("id"))

                if not event_id or event_id in events:
                    continue

                # Get title
                title = clean_text(event.get("title"))

                # Get start and end time
                if event.get("date_time") is None:
                    # JAFAR – THIS IS INCOMPLETE LOGIC:
                    # We cannot set an arbitrary hour of day as start time, there must be a date
                    # start_time = '12 a.m.'
                    start_time = ""
                else:
                    start_time = clean_text(event.get("date_iso"))

                if event.get("date2_time") is None:
                    # JAFAR – THIS IS INCOMPLETE LOGIC. read above
                    # end_time = '11:59 p.m.'
                    end_time = ""
                else:
                    end_time = clean_text(event.get("date2_iso"))

                # Get location
                location = clean_text(event.get("location"))

                # Get event summary/description
                summary = clean_html(event.get("summary"))

                # Summary/description could be in either summary or description field
                if summary is None:
                    summary = clean_html(event.get("description"))

                categories = ""
                # Get event types if any
                if event.get("event_types"):
                    categories = ",".join(event.get("event_types"))

                tags = ""
                # Get event tags if any
                if event.get("tags"):
                    tags = ",".join(event.get("tags"))

                org_name = ""
                if event.get("custom_organization"):
                    org_name = clean_text(event.get("custom_organization"))

                # Create event dictionary and add to list
                events[event_id] = {
                    "id": event_id,
                    "creation_time_stamp": (datetime.now(timezone.utc)).isoformat(),
                    "title": title,
                    "start_time": start_time,
                    "end_time": end_time,
                    "location": location,
                    "summary": summary,
                    "categories": categories,
                    "tags": tags,
                    "org_name": org_name,
                    "frequency": None,
                }

                cursor.execute(
                    """
                    INSERT or IGNORE INTO events (
                        id, creation_time_stamp, title, start_time, end_time, location, summary, categories, tags, org_name
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        event_id,
                        (datetime.now(timezone.utc)).isoformat(),
                        title,
                        start_time,
                        end_time,
                        location,
                        summary,
                        categories,
                        tags,
                        org_name,
                        # event["frequency"] # Will include soon
                    ),
                )

                if org_name:
                    # add_interest(cursor, org_name)
                    org_name = sanitize_name(clean_html(org_name))
                    interests = org_name.split(", ")
                    # corrects for potential incorrect splitting of name by adding in any org with a comma in their name
                    if "," in org_name:
                        interests.extend(
                            interest.name
                            for interest in INTERESTS_COMMA
                            if interest.name in org_name
                        )

                    for interest in interests:
                        add_event_interest(cursor, interest, event_id)
                if cursor.rowcount > 0:
                    inserted_count += 1

        connection.commit()
        print(f"Inserted {inserted_count} events into the database.")

    except Exception as e:
        connection.rollback()
        print(f"Error occurred during scraping: {e}")
    finally:
        connection.close()

    return events


# Helper function to find occurances of events with the same title.
# Limits search to events within the next month to avoid counting events that are far apart in time and not actually recurring.
# Updates the original events list with occurance information for multiple-occuring events.
def occurance_finder(events):
    # Filter events to only those from now till 30 days from now
    now = datetime.now()
    month_end = now + timedelta(days=30)

    events_within_30days = {}
    for event in events.values():
        start_dt = datetime.fromisoformat(event["start_time"])
        if start_dt > month_end:
            break
        events_within_30days[event["id"]] = event

    # Now find frequencies in the filtered events
    frequency_dict = dict()
    for event in events_within_30days.values():
        title = event["title"]
        if title not in frequency_dict:
            frequency_dict[title] = []
            frequency_dict[title].append(event.get("id"))
        else:
            frequency_dict[title].append(event.get("id"))

    # Update the original events list with frequencies for recurring events
    for title in frequency_dict:
        if len(frequency_dict[title]) > 1:
            first_id = frequency_dict[title][0]
            events[first_id]["occurances"] = []
            first = False
            for id in frequency_dict[title]:
                if not first:
                    events[first_id]["occurances"].append(
                        {
                            "start": events[id]["start_time"],
                            "end": events[id]["end_time"],
                        }
                    )
                    first = True
                else:
                    events[first_id]["occurances"].append(
                        {
                            "start": events[id]["start_time"],
                            "end": events[id]["end_time"],
                        }
                    )
                    events.pop(id, None)


# Tests if events were successfully inserted into the database by fetching and printing the first 5 events.
def test_scraping():
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, creation_time_stamp, title, start_time, end_time,
            location, summary, categories, tags, org_name, frequency
        FROM events
        LIMIT 5
    """)

    events = cursor.fetchall()

    cursor.execute("""
        SELECT id, name
        FROM interests
    """)
    interests = cursor.fetchall()

    cursor.execute("""
        SELECT event_id, interest_id
        FROM event_interests
    """)
    connection.close()

    print("\nFirst 5 events in database:")
    for event in events:
        print("ID:", event[0])
        print("\tCreated:", event[1])
        print("\tTitle:", event[2])
        print("\tStart:", event[3])
        print("\tEnd:", event[4])
        print("\tLocation:", event[5])
        print("\tSummary:", event[6])
        print("\tCategories:", event[7])
        print("\tTags:", event[8])
        print("\tOrg Name:", event[9])
        print("\tFrequency:", event[10])
        print()

    for interest in interests:
        # print("Interest ID:", interest[0])
        print("Interest Name:", interest[1])

    # for event_interest in event_interests:
    #     print("Event ID:", event_interest[0])
    #     print("Interest ID:", event_interest[1])
    #     print("Interest Name:", get_interest_by_id(event_interest[1], interests))
    #     print()


# run manually for testing
if __name__ == "__main__":
    initialize_database()
    populate_interests()
    events = scrape_events()
    # test_scraping()

    print("Number of events found:", len(events))
