#import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# Source: https://realpython.com/beautiful-soup-web-scraper-python/
# Source: https://scrapfly.io/blog/posts/web-scraping-with-playwright-and-python

BASE_URL = "https://events.grinnell.edu/"

# Helper function to clean text by removing extra whitespace
def clean_text(text):
    if text is None:
        return None
    # Replace all whitespace characters with a single space and trim leading/trailing whitespace
    return " ".join(text.split())

# # Helper function to extract organization/category tags from the event div classes
def clean_categories(class_list):
    categories = []

    for class_name in class_list:
        if class_name.startswith("lw_tag_"):
            cat_name = class_name.replace("lw_tag_", "")
            categories.append(cat_name)
        if class_name.startswith("lw_category_"):
            cat_name = class_name.replace("lw_category_", "")
            categories.append(cat_name)

    return categories


# Helper function to get the fully rendered HTML of the events page using Playwright
def get_rendered_html():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Open new page in browser
        page = browser.new_page()

        # Go to events website
        page.goto(BASE_URL)

        # Wait until event blocks actually appear in the rendered page
        page.wait_for_selector("div.lw_cal_event")

        html = page.content()

        browser.close()
        return html

# Q: What should id value be? event title?

def scrape_events():
    # Get the fully rendered webpage HTML using Playwright
    html = get_rendered_html()

    # Parse the HTML with beautiful soup
    soup = BeautifulSoup(html, "html.parser")

    # Find all event div blocks
    event_chunks = soup.find_all("div", class_="lw_cal_event")

    events = []

    # Loop through each event
    for chunk in event_chunks:

        # Get the classes attached to this event div
        class_list = chunk.get("class", [])

        # Extract category tags from the class names
        categories = clean_categories(class_list)

        # Parsing title
        title_div = chunk.find("div", class_="lw_events_title")
        title_element = title_div.find("a") if title_div else None        
        title = clean_text(title_element.get_text()) if title_element else None

        # Parsing event start and end times
        start_time_el = chunk.find("span", class_="lw_start_time")
        end_time_el = chunk.find("span", class_="lw_end_time")

        start_time = clean_text(start_time_el.get_text()) if start_time_el else None
        end_time = clean_text(end_time_el.get_text()) if end_time_el else None

        # Parsing event location
        location_el = chunk.find("div", class_="lw_events_location")
        location = clean_text(location_el.get_text()) if location_el else None

        # Parsing event description
        summary_el = chunk.find("div", class_="lw_events_summary")
        summary = clean_text(summary_el.get_text()) if summary_el else None

        # Some events only have one time stated in the end time, so we can move that to the start time and set end time to None
        if start_time is None and end_time is not None:
            start_time = end_time
            end_time = None

        # Storing event data in a dictionary and appending to events list
        events.append({
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
            "summary": summary,
            "categories": categories
        })

    return events

# run manually (for testing)
if __name__ == "__main__":
    events = scrape_events()
    print("Number of events found:", len(events))
    
    for event in events:
        print(event, "\n\n")