import unittest
from unittest.mock import MagicMock, patch
import sqlite3
from db_functions import *
from models import *

class TestMockObject(unittest.TestCase):

    def test_mock_object(self):
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

if __name__ == '__main__':
    unittest.main()