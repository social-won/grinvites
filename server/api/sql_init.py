import sqlite3

def initialize_database():
    #connect to the database (or create it if it doesn't exist)
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS events")
    cursor.execute("DROP TABLE IF EXISTS event_interests")
    cursor.execute("DROP TABLE IF EXISTS interests")

    #creates all necessary tables for the application
    #users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            display_name TEXT,
            calendar_type TEXT,
            prefer_notify INTEGER
    )
    ''')

    #interests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT
    )         
    ''')

    #user_interests table to link users and their interests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interests (
            user_id INTEGER,
            interest_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (interest_id) REFERENCES interests(id),
            PRIMARY KEY (user_id, interest_id)
    )
    ''')

    #events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creation_time_stamp TEXT NOT NULL,
            title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            location TEXT,
            summary TEXT,
            categories TEXT,
            tags TEXT,
            org_name TEXT,
            frequency TEXT
    )
    ''')

    #event_interests table to link events and their interests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_interests (
            event_id INTEGER,
            interest_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (interest_id) REFERENCES interests(id),
            PRIMARY KEY (event_id, interest_id)
    )
    ''')

    #commits the changes and closes the connection
    connection.commit()
    connection.close()
    #print("Database initialized successfully.")