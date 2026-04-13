import sqlite3
from scraper import scrape_events

#Adds a user to the database
def add_user(email, display_name=None, calendar_type=None, prefer_notify=0):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, display_name, calendar_type, prefer_notify)
        VALUES (?, ?, ?, ?)
    ''', (email, display_name, calendar_type, prefer_notify))
    connection.commit()
    connection.close()

#Gets a user via their email
def get_user_by_email(email):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    connection.close()
    return user

#Gets an event via its title
def get_event_by_title(title):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM events WHERE title = ?
    ''', (title,))
    event = cursor.fetchone()
    connection.close()
    return event

#Updates a user's interests or adds them if non exist.
def update_user_interests(email, interest_ids):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE email = ?
    ''', (email,))
    user_id = cursor.fetchone()[0]
    for interest_id in interest_ids:
        cursor.execute('''
                    INSERT OR IGNORE INTO user_interests (user_id, interest_id) VALUES (?, ?)
        ''', (user_id, interest_id))
    connection.commit()
    connection.close()

#Gets a user's interests via their email
def get_user_interests(email):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE email = ?
    ''', (email,))
    user_id = cursor.fetchone()[0]
    cursor.execute('''
        SELECT interest_id FROM user_interests WHERE user_id = ?
    ''', (user_id,))
    interest_ids = cursor.fetchall()
    user_interests = []
    for interest_id in interest_ids:
        user_interests.append(interest_id)
    connection.close()
    return user_interests

#Updates an event's interests or adds them if non exist.
def update_event_interests(event_title, interest_ids):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM events WHERE title = ?
    ''', (event_title,))
    event_id = cursor.fetchone()[0]
    for interest_id in interest_ids:
        cursor.execute('''
                    INSERT OR IGNORE INTO event_interests (event_id, interest_id) VALUES (?, ?)
        ''', (event_id, interest_id))
    connection.commit()
    connection.close()

#Gets an event's interests via its title
def get_event_interests(event_title):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM events WHERE title = ?
    ''', (event_title,))
    event_id = cursor.fetchone()[0]
    cursor.execute('''
        SELECT interest_id FROM event_interests WHERE event_id = ?
    ''', (event_id,))
    interest_ids = cursor.fetchall()
    event_interests = []
    for interest_id in interest_ids:
        event_interests.append(interest_id)
    connection.close()
    return event_interests

#Inserts events from the scraper into the database
def insert_events_into_db():
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

#gets all user information for a given event
def get_users_for_event(event_title):
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM events WHERE title = ?
    ''', (event_title))
    event_id = cursor.fetchone()[0]
    cursor.execute('''
        SELECT user_id FROM event_users WHERE event_id = ?
    ''', (event_id,))
    user_ids = cursor.fetchall()
    users = []
    for user_id in user_ids:
        users.append(user_id)
    connection.close()
    return users

#returns the email and display name in json for all users of a given event
def get_users_to_email(event_title):
    users = get_users_for_event(event_title)
    user_names = []
    user_emails = []
    for user in users:
        connection = sqlite3.connect('test_grinvites.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT email FROM users WHERE id = ?
        ''', (user,))
        user_email = cursor.fetchall()
        user_emails.append(user_email)
        cursor.execute('''
            SELECT display_name FROM users WHERE id = ?
        ''', (user,))
        user_name = cursor.fetchall()
        user_names.append(user_name)
        connection.close()
    return {"emails": user_emails, "names": user_names}
    