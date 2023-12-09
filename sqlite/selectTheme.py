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

def get_themes():
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Select all data
    table_name = 'themeSubs'
    select_all_query = f'SELECT theme, subreddit FROM {table_name};'
    cursor.execute(select_all_query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Organize the data into a dictionary
    data_dict = {}
    for row in rows:
        theme, subreddit = row
        if theme in data_dict:
            data_dict[theme].append(subreddit)
        else:
            data_dict[theme] = [subreddit]
    return data_dict