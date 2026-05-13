import json
import sqlite3, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # go up one level

from models import User
#from scraper import scrape_events

#switch to id being input
"""
Creates a connection to the database
Returns:
    A connection object to the database
"""
def get_db() -> sqlite3.Connection:
    path = os.getenv("DB_PATH", "database.db")
    conn = sqlite3.connect(path)
    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

"""
Adds a user to the database
Args:
    user: A User object containing the user's information
Returns:
    None
"""
def add_user(user: User):
    connection = get_db()
    cursor = connection.cursor()
    query = '''
        INSERT INTO users (id, email, display_name, invite_times, theme) VALUES (?, ?, ?, ?, ?)
        '''
    
    user_id = user.id
    email = user.email
    display_name = user.display_name
    invite_times = json.dumps(user.invite_times)
    theme = user.theme
    data = (user_id, email, display_name, invite_times, theme)

    cursor.execute(query, data)

    connection.commit()
    connection.close()

"""
Gets all users in the database
Returns:
    A list of tuples containing all users in the database
"""
def get_users():
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM users'''
    
    cursor.execute(query)

    users = cursor.fetchall()
    connection.close()
    return users

"""
Gets a user via their user_id
Args:
    user_id: The id of the user to get
Returns:
    A User object containing the user's information, or None if the user is not found"""
def get_user(user_id: str) -> User | None:
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM users WHERE id = ?'''
    data = (user_id,)

    cursor.execute(query, data)

    user = cursor.fetchone()
    connection.close()

    if not user:
        return None

    column_names = [col[0] for col in cursor.description]
    user_dict = dict(zip(column_names, user))
    user_dict["invite_times"] = json.loads(user_dict["invite_times"] or "{}")

    return User(**user_dict)

"""
Gets a user via their email
Args:
    user_email: The email of the user to get
Returns:
    A tuple containing the user's information, or None if the user is not found"""
def get_user_by_email(user_email):
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM users WHERE email = ?'''
    data = (user_email,)

    cursor.execute(query, data)

    user = cursor.fetchone()
    connection.close()
    return user

"""
Gets an event via its ID
Args:
    event_id: The ID of the event to get
Returns:
    A tuple containing the event's information, or None if the event is not found
"""
def get_event_by_id(event_id): 
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM events WHERE id = ?'''
    data = (event_id,)

    cursor.execute(query, data)

    event = cursor.fetchone()
    connection.close()
    return event

"""
Updates a user's interests in the database
Args:
    email: The email of the user to update
    interest_ids: A list of interest IDs to associate with the user
Returns:
    None
"""
def update_user_interests(email, interest_ids):
    connection = get_db()
    cursor = connection.cursor()

    select_query = '''SELECT id FROM users WHERE email = ?'''
    user_email = (email,)

    cursor.execute(select_query, user_email)
    user_id = cursor.fetchone()[0]

    insert_query = '''INSERT OR IGNORE INTO user_interests (user_id, interest_id) VALUES (?, ?)'''

    for interest_id in interest_ids:
        data = (user_id, interest_id)
        cursor.execute(insert_query, data)

    connection.commit()
    connection.close()

"""
Gets a user's interests from the database
Args:
    email: The email of the user to get interests for
Returns:
    A list of interest IDs associated with the user
"""
def get_user_interests(user_id):
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT i.* FROM interests i INNER JOIN user_interests ui ON i.id = ui.interest_id WHERE ui.user_id = ?'''
    data = (user_id,)

    cursor.execute(query, data)

    interests = cursor.fetchall()
    connection.close()

    # Convert to list of dicts
    column_names = [col[0] for col in cursor.description]
    interests = [dict(zip(column_names, row)) for row in interests]
    return interests

"""
Gets all interests in the database
Returns:
    A list of dicts containing all interests in the database
"""
def get_interests():
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM interests'''
    
    cursor.execute(query)

    interests = cursor.fetchall()
    if not interests:
        return
    
    column_names = [col[0] for col in cursor.description]
    interests = [dict(zip(column_names, row)) for row in interests]

    connection.close()
    return interests

"""
Adds an event to the database
Args:
    title: The title of the event
    start_time: The start time of the event
    end_time: The end time of the event
    location: The location of the event
    summary: A summary of the event
    categories: A list of categories for the event
    tags: A list of tags for the event
    org_name: The name of the organization hosting the event
    frequency: The frequency of the event
Returns:
    None
"""
def add_event(title, start_time, end_time, location, summary = None, categories = None, tags = None, org_name = None, frequency = None):
    connection = get_db()
    cursor = connection.cursor()

    query = '''INSERT INTO events (creation_time_stamp, title, start_time, end_time, location, summary, categories, tags, org_name, frequency) VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = (title, start_time, end_time, location, summary, categories, tags, org_name, frequency)
    
    cursor.execute(query, data)

    connection.commit()
    connection.close()
"""
Gets all events in the database
Returns:
    A list of tuples containing all events in the database
"""
def get_events():
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM events'''

    cursor.execute(query)

    events = cursor.fetchall()
    connection.close()
    return events

"""
Gets an event via its title
Args:
    title: The title of the event to get
Returns:
    A tuple containing the event's information, or None if the event is not found"""
def get_event_by_title(title):
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM events WHERE title = ?'''
    data = (title,)

    cursor.execute(query, data)

    event = cursor.fetchone()
    connection.close()
    return event

"""
Gets events that start within a given time range
Args:
    initial_start_time: The start time of the event
    final_start_time: The end time of the event
Returns:
    A list of tuples containing the events within the specified time range
"""
def get_event_by_time(initial_start_time, final_start_time):
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT * FROM events WHERE start_time >= ? AND start_time <= ?'''
    data = (initial_start_time, final_start_time)

    cursor.execute(query, data)

    events = cursor.fetchall()
    connection.close()
    return events

"""
Updates an event's interests in the database
Args:
    event_title: The title of the event to update
    interest_ids: A list of interest IDs to associate with the event
Returns:
    None
"""
def update_event_interests(event_title, interest_ids):
    connection = get_db()
    cursor = connection.cursor()

    select_query = '''SELECT id FROM events WHERE title = ?'''
    event_title_data = (event_title,)

    cursor.execute(select_query, event_title_data)
    event_id = cursor.fetchone()[0]

    insert_query = '''INSERT OR IGNORE INTO event_interests (event_id, interest_id) VALUES (?, ?)'''
    
    for interest_id in interest_ids:
        data = (event_id, interest_id)
        cursor.execute(insert_query, data)

    connection.commit()
    connection.close()

"""
Gets an event's interests from the database
Args:
    event_title: The title of the event to get interests for
Returns:
    A list of interest IDs associated with the event
"""
def get_event_interests(event_title):
    connection = get_db()
    cursor = connection.cursor()

    query_events = '''SELECT id FROM events WHERE title = ?'''
    event_title_data = (event_title,)
    cursor.execute(query_events, event_title_data)
    event_id = cursor.fetchone()[0]

    query_interests = '''
        SELECT interest_id FROM event_interests WHERE event_id = ?
        '''
    data = (event_id,)

    cursor.execute(query_interests, data)

    interest_ids = cursor.fetchall()
    event_interests = [row[0] for row in interest_ids]
    connection.close()
    return event_interests

"""
inserts all events into the database
Args:    events: A list of dicts containing the events to insert into the database
Returns:    None
"""
def insert_events_into_db(events):
    connection = get_db()
    cursor = connection.cursor()
    inserted_count = 0

    query = '''INSERT INTO events (title, org_name, description, start_time, end_time, location, frequency) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    for event in events:
        data = (event["title"],
                None,
                event["summary"],
                event["start_time"],
                event["end_time"],
                event["location"],
                None)
        cursor.execute(query, data)
        inserted_count += 1

    connection.commit()
    connection.close()
    print(f"Inserted {inserted_count} events into the database.")

"""
Gets a list of events based on their start times
Args:    start_time: The start time of the event to get
Returns:    A list of tuples containing the events with the specified start time
"""
def get_event_id_by_time(start_time):
    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT id FROM events WHERE start_time = ?'''
    data = (start_time,)

    cursor.execute(query, data)

    event_id = cursor.fetchall()
    event_ids = [row[0] for row in event_id]
    connection.close()
    return event_ids

"""
Gets a list of user IDs for users that have interests that match an event's interests
Args:    event_id: The ID of the event to get users for
Returns:    A list of user IDs for users that have interests that match the event's interests
"""
def get_users_for_event(event_id):
    connection = get_db()
    cursor = connection.cursor()

    query_events = '''SELECT interest_id FROM event_interests WHERE event_id = ?'''
    data = (event_id,)
    cursor.execute(query_events, data)
    interest_ids = [row[0] for row in cursor.fetchall()]

    user_ids = []
    query_user_interests = '''SELECT user_id FROM user_interests WHERE interest_id = ?'''
    for interest_id in interest_ids:
        data = (interest_id,)
        cursor.execute(query_user_interests, data)
        user_ids.extend(row[0] for row in cursor.fetchall())

    connection.close()
    return user_ids

"""
Gets the emails and names of users that should be emailed for an event
Args:    event_id: The ID of the event to get users for
Returns:    A dict containing the emails and names of users that should be emailed for the event
"""
def get_users_to_email(event_id):
    users = get_users_for_event(event_id)
    user_names = []
    user_emails = []
    query_emails = '''SELECT email FROM users WHERE id = ?'''
    query_names = '''SELECT display_name FROM users WHERE id = ?'''
    
    connection = get_db()
    cursor = connection.cursor()

    for user in users:
        data = (user,)

        cursor.execute(query_emails, data)
        user_email = cursor.fetchall()
        user_emails.append(user_email)

        cursor.execute(query_names, data)
        user_name = cursor.fetchall()
        user_names.append(user_name)
    
    connection.close()
    return {"emails": user_emails, "names": user_names}

"""
adds an event to the list of events a user has been emailed about
Args:    event_id: The ID of the event to add to the user's emailed list
Returns:    None
"""
def add_user_events_emailed(event_id):
    users = get_users_for_event(event_id)
    connection = get_db()
    cursor = connection.cursor()
    event_id_str = str(event_id) + ","
    query = '''UPDATE users SET events_emailed = ? WHERE id = ?'''
    

    for user in users:
        data = (event_id_str, user)
        cursor.execute(query, data)

    connection.commit()
    connection.close()
"""
Checks if a user has already been emailed about an event
Args:    user_id: The ID of the user to check
         event_id: The ID of the event to check
Returns:    True if the user has already been emailed about the event, False otherwise
"""
def if_user_emailed_for_event(user_id, event_id):
    users_emailed_events = []

    connection = get_db()
    cursor = connection.cursor()

    query = '''SELECT events_emailed FROM users WHERE id = ?'''
    data = (user_id,)

    cursor.execute(query, data)
    events_emailed = cursor.fetchone()[0]

    if events_emailed:
        users_emailed_events = events_emailed.split(",")
    
    for event in users_emailed_events:
        if event == str(event_id):
            return True
        
    return False