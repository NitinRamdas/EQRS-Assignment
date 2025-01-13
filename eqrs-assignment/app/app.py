from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host='db', 
        database='hello_world', 
        user='user', 
        password='password'
    )
    return conn

@app.route('/')
def hello_world():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT message FROM greetings LIMIT 1;')
    greeting = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({'message': greeting[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
