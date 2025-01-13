import unittest
from app import app, get_db_connection
import psycopg2
from unittest.mock import patch

class AppTestCase(unittest.TestCase):

    def setUp(self):
      
        app.config['TESTING'] = True
        self.client = app.test_client()

        self.test_conn = get_db_connection()
        self.test_cursor = self.test_conn.cursor()
        self.test_cursor.execute("CREATE TABLE IF NOT EXISTS greetings (id SERIAL PRIMARY KEY, message VARCHAR(255))")
        self.test_cursor.execute("INSERT INTO greetings (message) VALUES ('Hello, World!')")
        self.test_conn.commit()

    def tearDown(self):
      
        self.test_cursor.execute("DROP TABLE IF EXISTS greetings")
        self.test_conn.commit()
        self.test_conn.close()

    def test_hello_world(self):
      
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World!', response.data)

    @patch('psycopg2.connect')
    def test_db_connection(self, mock_connect):
      
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ['Hello from mock DB!']

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello from mock DB!', response.data)

if __name__ == '__main__':
    unittest.main()
