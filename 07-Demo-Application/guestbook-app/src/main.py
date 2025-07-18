import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the database."""
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return conn

# Create the table if it doesn't exist
try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS entries (id serial PRIMARY KEY, username varchar(50) NOT NULL, message text NOT NULL, timestamp timestamp DEFAULT CURRENT_TIMESTAMP);')
    conn.commit()
    cur.close()
    conn.close()
except psycopg2.OperationalError as e:
    print(f"Could not connect to database to initialize schema: {e}")

@app.route('/')
def index():
    """Renders the main page with guestbook entries."""
    page_title = os.environ.get('APP_TITLE', 'Kubernetes Guestbook')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM entries ORDER BY timestamp DESC;')
        entries = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        entries = []
        print(f"Error fetching entries: {e}")
        
    return render_template('index.html', entries=entries, page_title=page_title)

@app.route('/add', methods=['POST'])
def add_entry():
    """Adds a new entry to the guestbook."""
    username = request.form['username']
    message = request.form['message']
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO entries (username, message) VALUES (%s, %s)', (username, message))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error adding entry: {e}")
        
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)