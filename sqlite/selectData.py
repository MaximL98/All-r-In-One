import sqlite3

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

def get_data(theme):
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Select all data
    table_name = 'data'
    select_all_query = f"SELECT * FROM {table_name} WHERE theme = '{theme}';"
    cursor.execute(select_all_query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    return rows




