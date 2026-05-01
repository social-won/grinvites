import json
import sqlite3, os

from models import User
#from scraper import scrape_events

#switch to id being input

def get_db() -> sqlite3.Connection:
    path = os.getenv("DB_PATH", "database.db")
    conn = sqlite3.connect(path)
    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#Adds a user to the database
def add_user(user: User):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO users (id, email, display_name, invite_times)
        VALUES (?, ?, ?, ?)
    ''', (user.id, user.email, user.display_name, json.dumps(user.invite_times)))
    connection.commit()
    connection.close()

def get_users():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM users
    ''')
    users = cursor.fetchall()
    connection.close()
    return users

#Gets a user via their email
def get_user(user_id: str) -> User | None:
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE id = ?
    ''', (user_id,))
    user = cursor.fetchone()
    connection.close()

    if not user:
        return None

    column_names = [col[0] for col in cursor.description]
    user_dict = dict(zip(column_names, user))
    user_dict["invite_times"] = json.loads(user_dict["invite_times"] or "{}")

    return User(**user_dict)

#Gets a user via their email
def get_user_by_email(email):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    connection.close()
    return user

def get_event_by_id(event_id): 
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM events WHERE id = ?
    ''', (event_id,))
    event = cursor.fetchone()
    connection.close()
    return event

#Updates a user's interests or adds them if non exist.
def update_user_interests(email, interest_ids):
    connection = get_db()
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

#Gets a user's interests via their user_id
def get_user_interests(user_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT i.* FROM interests i
        INNER JOIN user_interests ui ON i.id = ui.interest_id
        WHERE ui.user_id = ?
    ''', (user_id,))
    interests = cursor.fetchall()
    connection.close()
    return interests

#Get all interests
def get_interests():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM interests
    ''')
    interests = cursor.fetchall()
    if not interests:
        return
    
    column_names = [col[0] for col in cursor.description]
    interests = [dict(zip(column_names, row)) for row in interests]

    connection.close()
    return interests

def add_event(title, start_time, end_time, location, summary = None, categories = None, tags = None, org_name = None, frequency = None):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO events (creation_time_stamp, title, start_time, end_time, location, summary, categories, tags, org_name, frequency)
        VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, start_time, end_time, location, summary, categories, tags, org_name, frequency))
    connection.commit()
    connection.close()

def get_events():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM events
    ''')
    events = cursor.fetchall()
    connection.close()
    return events

#Gets an event via its title
def get_event_by_title(title):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM events WHERE title = ?
    ''', (title,))
    event = cursor.fetchone()
    connection.close()
    return event

def get_event_by_time(initial_start_time, final_start_time):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM events WHERE start_time >= ? AND start_time <= ?
    ''', (initial_start_time, final_start_time))
    events = cursor.fetchall()
    connection.close()
    return events

#Updates an event's interests or adds them if non exist.
def update_event_interests(event_title, interest_ids):
    connection = get_db()
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
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM events WHERE title = ?
    ''', (event_title,))
    event_id = cursor.fetchone()[0]
    cursor.execute('''
        SELECT interest_id FROM event_interests WHERE event_id = ?
    ''', (event_id,))
    interest_ids = cursor.fetchall()
    event_interests = [row[0] for row in interest_ids]
    connection.close()
    return event_interests

#Inserts events from the scraper into the database
def insert_events_into_db(events):
    connection = get_db()
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

def get_event_id_by_time(start_time):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM events WHERE start_time = ?
    ''', (start_time,))
    event_id = cursor.fetchall()
    event_ids = [row[0] for row in event_id]
    connection.close()
    return event_ids

#gets all user information for a given event
def get_users_for_event(event_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT interest_id FROM event_interests WHERE event_id = ?', (event_id,))
    interest_ids = [row[0] for row in cursor.fetchall()]

    user_ids = []
    for interest_id in interest_ids:
        cursor.execute('SELECT user_id FROM user_interests WHERE interest_id = ?', (interest_id,))
        user_ids.extend(row[0] for row in cursor.fetchall())

    connection.close()
    return user_ids

#returns the email and display name in json for all users of a given event
def get_users_to_email(event_id):
    users = get_users_for_event(event_id)
    user_names = []
    user_emails = []
    for user in users:
        connection = get_db()
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