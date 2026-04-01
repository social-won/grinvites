import sqlite3

def init_db():
    #connect to the database (or create it if it doesn't exist)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

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
            type TEXT NOT NULL
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
            title TEXT NOT NULL,
            org_name TEXT,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            location TEXT
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
    #connect to the database (or create it if it doesn't exist)
    connection = sqlite3.connect('test_grinvites.db')
    cursor = connection.cursor()

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
            type TEXT NOT NULL
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
            title TEXT NOT NULL,
            org_name TEXT,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            location TEXT
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

def add_user(email, display_name=None, calendar_type=None, prefer_notify=0):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, display_name, calendar_type, prefer_notify)
        VALUES (?, ?, ?, ?)
    ''', (email, display_name, calendar_type, prefer_notify))
    connection.commit()
    connection.close()

def get_user_by_email(email):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    connection.close()
    return user

init_db()
add_user("juddbrau@gmail.com", "Judd Brau", "Google Calendar")
user = get_user_by_email("juddbrau@gmail.com")
print(user)