import sqlite3
from database import insert_comments

# Connect to the SQLite database file
# Function getting database connection
def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")

    return conn

conn = create_connection('sqlite/allR.db')

def get_comments(post_id):
    insert_comments(post_id, 10)
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Select all comments
    select_query = "SELECT content FROM comments WHERE post_id = ?"
    cursor.execute(select_query, (post_id,))

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    return rows





