import unittest
import os
from db_functions import *

# add_user, add_event, get_users, get_events, get_user_by_email, update_user_interests, get_user_interests, update_event_interests, get_event_interests, get_event_by_title
from sql_init import initialize_database


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create a new test database and tables before each test
        if os.path.exists("test_grinvites.db"):
            os.remove("test_grinvites.db")
        initialize_database()

    def tearDown(self):
        # Close the connection and delete the test database after each test
        os.remove("test_grinvites.db")

    def test_add_and_get_user(self):
        add_user("test@example.com", "Test User", "Google Calendar", 1)
        user = get_user_by_email("test@example.com")
        self.assertEqual(user[0], 1)  # ID should be 1 for the first user
        self.assertEqual(user[1], "test@example.com")
        self.assertEqual(user[2], "Test User")
        self.assertEqual(user[3], "Google Calendar")
        self.assertEqual(user[4], 1)

    def test_update_and_get_user_interests(self):
        # Add a user and some interests
        add_user("test@example.com", "Test User", "Google Calendar", 1)
        update_user_interests("test@example.com", ["Interest 1", "Interest 2"])
        interests = get_user_interests("test@example.com")
        self.assertEqual(interests[0], "Interest 1")
        self.assertEqual(interests[1], "Interest 2")

    def test_get_users(self):
        add_user("test@example.com", "Test User", "Google Calendar", 1)
        add_user("test2@example.com", "Test User 2", "Outlook Calendar", 2)
        users = get_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0][0], 1)  # ID of first user
        self.assertEqual(users[1][0], 2)  # ID of second user
        self.assertEqual(users[0][1], "test@example.com")
        self.assertEqual(users[1][1], "test2@example.com")
        self.assertEqual(users[0][2], "Test User")
        self.assertEqual(users[1][2], "Test User 2")
        self.assertEqual(users[0][3], "Google Calendar")
        self.assertEqual(users[1][3], "Outlook Calendar")
        self.assertEqual(users[0][4], 1)
        self.assertEqual(users[1][4], 2)

    # def test_get_events(self):
    # needs to be updated for new structure of events table
    # add_event('Event 1', 'Org 1', 'Description 1', '2024-01-01T10:00:00', '2024-01-01T12:00:00', 'Location 1', 'None')
    # events = get_events()
    # self.assertEqual(len(events), 1)
    # self.assertEqual(events[0][0], 1)  # ID of first event
    # self.assertEqual(events[0][1], 'Event 1')
    # self.assertEqual(events[0][2], 'Org 1')
    # self.assertEqual(events[0][3], 'Description 1')
    # self.assertEqual(events[0][4], '2024-01-01T10:00:00')
    # self.assertEqual(events[0][5], '2024-01-01T12:00:00')
    # self.assertEqual(events[0][6], 'Location 1')
    # self.assertEqual(events[0][7], 'None')

    def test_update_and_get_event_interests(self):
        add_event(
            "Event 1",
            "Org 1",
            "Description 1",
            "2024-01-01T10:00:00",
            "2024-01-01T12:00:00",
            "Location 1",
            "None",
        )
        update_event_interests("Event 1", ["Interest 1", "Interest 2"])
        interests = get_event_interests("Event 1")
        self.assertEqual(interests[0], "Interest 1")
        self.assertEqual(interests[1], "Interest 2")

    def test_get_users_for_event(self):
        add_user("test@example.com", "Test User", "Google Calendar", 1)
        add_event(
            "Event 1",
            "Org 1",
            "Description 1",
            "2024-01-01T10:00:00",
            "2024-01-01T12:00:00",
            "Location 1",
            "None",
        )
        update_event_interests("Event 1", ["Interest 1"])
        update_user_interests("test@example.com", ["Interest 1"])
        # calling it for the night not sure what is going on here. Will talk to Judd and Grant tommorrow
        users = get_users_for_event(get_event_by_title("Event 1")[0])
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_get_event_by_time(self):
        add_event(
            "Event 1",
            "2024-01-01T10:00:00",
            "2024-01-01T12:00:00",
            "Location 1",
            "None",
        )
        add_event(
            "Event 2",
            "2024-01-02T10:00:00",
            "2024-01-02T12:00:00",
            "Location 2",
            "None",
        )
        events = get_event_by_time("2024-01-01T00:00:00", "2024-01-01T23:59:59")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0][0], 1)  # ID of first event
        self.assertEqual(events[0][2], "Event 1")
        self.assertEqual(events[0][3], "2024-01-01T10:00:00")
        self.assertEqual(events[0][4], "2024-01-01T12:00:00")
        self.assertEqual(events[0][5], "Location 1")
        self.assertEqual(events[0][6], "None")


if __name__ == "__main__":
    unittest.main()
