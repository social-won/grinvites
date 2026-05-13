import unittest
from unittest.mock import MagicMock, patch
import sqlite3
from db_functions import *
from models import *

class TestMockObject(unittest.TestCase):

    def test_get_user(self):
        # Mock connect method
        sqlite3.connect = MagicMock()
        mock_cursor = sqlite3.connect.return_value.cursor.return_value

        test_user = User(id='abcdef', email='test@example.com', display_name='Test User', invite_times={}, theme='light', events_emailed='none')
        test_user.invite_times = json.dumps(test_user.invite_times)
        #mock_cursor.fetchone.return_value = test_user.__dict__.values()  # Return the user attributes as a tuple
        mock_cursor.description = [('id',), ('email',), ('display_name',), ('invite_times',), ('theme',), ('events_emailed',)]
        mock_cursor.fetchone.return_value = ('abcdef', 'test@example.com', 'Test User', '{}', 'light', 'none')

        mock_user = get_user('abcdef')

        # Test the attributes
        mock_cursor.execute.assert_called_with("SELECT * FROM users WHERE id = ?", ('abcdef',))
        self.assertEqual(mock_user.id, test_user.id)

    def test_get_users(self):
        # Mock connect method
        sqlite3.connect = MagicMock()
        mock_cursor = sqlite3.connect.return_value.cursor.return_value

        test_user1 = User(id='abcdef', email='test1@example.com', display_name='Test User 1', invite_times={}, theme='light', events_emailed='none')
        test_user2 = User(id='ghijkl', email='test2@example.com', display_name='Test User 2', invite_times={}, theme='dark', events_emailed='none')

        mock_cursor.fetchall.return_value = [
            ('abcdef', 'test1@example.com', 'Test User 1', '{}', 'light', 'none'),
            ('ghijkl', 'test2@example.com', 'Test User 2', '{}', 'dark', 'none')
        ]

        mock_users = get_users()

        # Test the attributes
        mock_cursor.execute.assert_called_with("SELECT * FROM users")
        self.assertEqual(len(mock_users), 2)
        self.assertEqual(mock_users[0][0], test_user1.id)
        self.assertEqual(mock_users[1][0], test_user2.id)

    def test_get_user_by_email(self):
        # Mock connect method
        sqlite3.connect = MagicMock()
        mock_cursor = sqlite3.connect.return_value.cursor.return_value

        test_user1 = User(id='abcdef', email='test1@example.com', display_name='Test User 1', invite_times={}, theme='light', events_emailed='none')
        mock_cursor.fetchone.return_value = ('abcdef', 'test1@example.com', 'Test User 1', '{}', 'light', 'none')

        mock_user = get_user_by_email('test1@example.com')

        # Test the attributes
        mock_cursor.execute.assert_called_with("SELECT * FROM users WHERE email = ?", ('test1@example.com',))
        self.assertEqual(mock_user[0], test_user1.id)

    def test_update_user_interests(self):
        # Mock connect method
        sqlite3.connect = MagicMock()
        mock_cursor = sqlite3.connect.return_value.cursor.return_value

        test_user = User(id='abcdef', email='test@example.com', display_name='Test User', invite_times={}, theme='light', events_emailed='none')
        interests = ['music', 'sports']
       

        mock_cursor.fetchone.return_value = [(1, 'music'), (2, 'sports')]
        
        mock_cursor.description = [('id',), ('name',)]
        update_user_interests('abcdef', interests)
        mock_user_interests = get_user_interests('abcdef')

        # Test the attributes
        mock_cursor.execute.assert_called_with('SELECT i.* FROM interests i INNER JOIN user_interests ui ON i.id = ui.interest_id WHERE ui.user_id = ?', ('abcdef',))
        self.assertEqual(mock_user_interests, get_user_interests(test_user.id))

    def test_get_user_interests(self):
        # Mock connect method
        sqlite3.connect = MagicMock()
        mock_cursor = sqlite3.connect.return_value.cursor.return_value

        test_user = User(id='abcdef', email='test@example.com', display_name='Test User', invite_times={}, theme='light', events_emailed='none')
        interests = ['music', 'sports']
        mock_cursor.fetchall.return_value = [(1, 'music'), (2, 'sports')]
        mock_cursor.description = [('id',), ('name',)]

        update_user_interests('abcdef', interests)

        mock_user_interests = get_user_interests('abcdef')

        mock_cursor.execute.assert_called_with('SELECT i.* FROM interests i INNER JOIN user_interests ui ON i.id = ui.interest_id WHERE ui.user_id = ?', ('abcdef',))
        self.assertEqual(mock_user_interests, get_user_interests(test_user.id))

if __name__ == '__main__':
    unittest.main()