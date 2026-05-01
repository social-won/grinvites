import sqlite3
from server.api.db_functions import get_db
from sql_init import initialize_database
from scraper import scrape_events

# Populate the database with the events scraped from the grinnell events website.
# FIX: Check for duplicates before inserting. Does not do that yet.

def insert_events_into_db():
    initialize_database()
    events = scrape_events()

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM events")

    inserted_count = 0

    for event in events:
        cursor.execute('''
            INSERT INTO events (
                title, org_name, description, start_time, end_time, location
            )
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            event["title"],
            None,
            event["summary"],
            event["start_time"],
            event["end_time"],
            event["location"],
            # event["frequency"] # Will include soon
        ))
        inserted_count += 1

        #for event in events:
         #   print(event["title"], "\n\n")

    connection.commit()
    connection.close()

    print("Inserted " + str(inserted_count) + " events into the database.")

# Tests if events were successfully inserted into the database by fetching and printing the first 5 events.
def test_db():
    connection = get_db()
    cursor = connection.cursor()
    
    cursor.execute('''
        SELECT id, title, start_time, location FROM events LIMIT 5
    ''')
    
    events = cursor.fetchall()
    connection.close()
    
    print("\nFirst 5 events in database:")
    for event in events:
        print("  ID: " + str(event[0]) + ", Title: " + str(event[1]) + ", Start: " + str(event[2]) +
              ", Location: " + str(event[3]))


if __name__ == "__main__":
    insert_events_into_db()
    test_db()

