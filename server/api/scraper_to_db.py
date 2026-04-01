import sqlite3
from sql_init import initialize_database
from scraper import scrape_events

# Populate the database with the events scraped from the grinnell events website.
# FIX: Check for duplicates before inserting. Does not do that yet.

def insert_events_into_db():
    initialize_database()
    events = scrape_events()

    connection = sqlite3.connect("test_grinvites.db")
    cursor = connection.cursor()

    inserted_count = 0

    for event in events:
        cursor.execute('''
            INSERT INTO events (
                title, org_name, description, start_time, end_time, location, frequency
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event["title"],
            None,
            event["summary"],
            event["start_time"],
            event["end_time"],
            event["location"],
            None
        ))
        inserted_count += 1

    connection.commit()
    connection.close()

    print(f"Inserted {inserted_count} events into the database.")


if __name__ == "__main__":
    insert_events_into_db()

