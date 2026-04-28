import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from sql_init import initialize_database

# Source: https://realpython.com/beautiful-soup-web-scraper-python/
# Source: https://scrapfly.io/blog/posts/web-scraping-with-playwright-and-python
# Source: https://github.com/seehorne/GetGrinnected

JSON_URL = "https://events.grinnell.edu/live/json/events/response_fields/all/paginate"


# Helper function to clean text by removing extra whitespace
def clean_text(text):
    if text is None:
        return None
    return " ".join(str(text).split())


# Helper function to remove HTML tags from JSON fields like summary/description
def clean_html(html_text):
    if html_text is None:
        return None

    soup = BeautifulSoup(html_text, "html.parser")
    return clean_text(soup.get_text(" "))


# Helper function to fetch one JSON page
def get_json_page(page_num):
    url = JSON_URL + "?page=" + str(page_num)

    return requests.get(url).json() 


# Scrape events from the LiveWhale JSON endpoint
def scrape_events():
    initialize_database()

    connection = sqlite3.connect("test_grinvites.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM events")

    events = {}

    inserted_count = 0

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

            #Get id
            id = clean_text(event.get("id"))

            if id in events:
                continue

            # Get title
            title = clean_text(event.get("title"))

            # Get start and end time
            if event.get("date_time") is None:
                start_time = "12 a.m."
            else:
                start_time = clean_text(event.get("date_iso"))

            if event.get("date2_time") is None:
                end_time = "11:59 p.m."
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
            events[id] = {
                "id": id,
                "creation_time_stamp": (datetime.now(timezone.utc)).isoformat(),
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
                "summary": summary,
                "categories": categories,
                "tags": tags,
                "org_name": org_name,
                "frequency": None
            }

            cursor.execute('''
                INSERT INTO events (
                    id, creation_time_stamp, title, start_time, end_time, location, summary, categories, tags, org_name
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                id,
                (datetime.now(timezone.utc)).isoformat(),
                title,
                start_time,
                end_time,
                location,
                summary,
                categories,
                tags,
                org_name
                # event["frequency"] # Will include soon
            ))

            inserted_count += 1
        
    connection.commit()
    connection.close()

    print("Inserted " + str(inserted_count) + " events into the database.")

    return events
# Helper function to find frequency of events with the same title.
# Limits search to events within the next month to avoid counting events that are far apart in time and not actually recurring. 
# Updates the original events list with frequency information for recurring events.
# def frequency_finder(events):
#     # Filter events to only those from now till 30 days from now
#     now = datetime.now()
#     month_start = now
#     month_end = now + timedelta(days=30)
    
#     events_within_30days = {}
#     for event in events.values():
#         start_dt = datetime.fromisoformat(event["start_time"])
#         if start_dt > month_end:
#             break
#         events_within_30days[event["id"]] = event

#     # Now find frequencies in the filtered events
#     frequency_dict = dict()
#     for event in events_within_30days.values():
#         title = event["title"]
#         if title not in frequency_dict:
#             frequency_dict[title] = []
#             frequency_dict[title].append(event.get("id"))
#         else:
#             frequency_dict[title].append(event.get("id"))

#     # Update the original events list with frequencies for recurring events
#     for title in frequency_dict:
#         if len(frequency_dict[title]) > 2:

#             for id in frequency_dict[title]:
#                 events[id]["frequency"] = 

# Tests if events were successfully inserted into the database by fetching and printing the first 5 events.
def test_db():
    connection = sqlite3.connect("test_grinvites.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT id, creation_time_stamp, title, start_time, end_time,
            location, summary, categories, tags, org_name, frequency
        FROM events
        LIMIT 5
    ''')
    
    events = cursor.fetchall()
    connection.close()
    
    print("\nFirst 5 events in database:")
    for event in events:
        print("ID:", event[0])
        print("Created:", event[1])
        print("Title:", event[2])
        print("Start:", event[3])
        print("End:", event[4])
        print("Location:", event[5])
        print("Summary:", event[6])
        print("Categories:", event[7])
        print("Tags:", event[8])
        print("Org Name:", event[9])
        print("Frequency:", event[10])
        print()
        

# run manually for testing
if __name__ == "__main__":
    events = scrape_events()
    test_db()
    
    print("Number of events found:", len(events))
