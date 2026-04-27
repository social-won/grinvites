import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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
    events = []

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

            # Get title
            title = clean_text(event.get("title"))

            # Get start and end time
            if event.get("date_time") is None:
                start_time = "12 a.m."
            else:
                start_time = clean_text(event.get("date_time"))

            if event.get("date2_time") is None:
                end_time = "11:59 p.m."
            else:
                end_time = clean_text(event.get("date2_time"))

            # Get location
            location = clean_text(event.get("location"))

            # Get event summary/description
            summary = clean_html(event.get("summary"))

            # Summary/description could be in either summary or description field
            if summary is None:
                summary = clean_html(event.get("description"))

            categories = []
            # Get event types if any
            if event.get("event_types"):  
                categories = event.get("event_types")

            tags = []
            # Get event tags if any
            if event.get("tags"):
                tags = event.get("tags")

            # Create event dictionary and add to list                        
            events.append({
                "id": id,
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
                "summary": summary,
                "categories": categories,
                "tags": tags,
                "frequency": None
            })

    return events

# Helper function to find frequency of events with the same title. O(n) runtime
# Limits search to events within the next month to avoid counting events that are far apart in time and not actually recurring. 
# Updates the original events list with frequency information for recurring events.
# def frequency_finder(events):
#     # Filter events to only those from now till 30 days from now
#     now = datetime.now()
#     month_start = now
#     month_end = now + timedelta(days=30)
    
#     filtered_events = []
#     for event in events:
#         start_dt = datetime.fromisoformat(event["start_time"])
#         if start_dt > month_end:
#             break
#         filtered_events.append(event)
    
#     # Now find frequencies in the filtered events
#     frequency_dict = dict()
#     for event in filtered_events:
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
#                 events.get


# run manually for testing
if __name__ == "__main__":
    events = scrape_events()

    for event in events:
        print(event, "\n\n")
    
    print("Number of events found:", len(events))