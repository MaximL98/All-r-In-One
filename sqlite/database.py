import sqlite3
from sqlite3 import Error
import sys
from paths import PATH_TO_REDDIT_API
sys.path.append(PATH_TO_REDDIT_API)
from redditConn import DATA

# Function getting database connection
def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn

conn = sqlite3.connect('sqlite/allR.db')

# Function for getting query and executing it.
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data is not None:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def delete_rows(connection, table_name, start_row, end_row):
    delete_query = f'DELETE FROM {table_name} WHERE rowid BETWEEN {start_row} AND {end_row};'
    cursor = connection.cursor()
    try:
        cursor.execute(delete_query)
        connection.commit()
        print(f"Rows {start_row} to {end_row} deleted successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")




# Create data table
create_data_table = """
CREATE TABLE IF NOT EXISTS data (
    theme TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
"""
execute_query(conn, create_data_table)  


# SQL command to drop the table
'''table_name = 'data'
drop_table_sql = f'DROP TABLE IF EXISTS {table_name};'
execute_query(conn, drop_table_sql)'''


# Define the SQL command to insert data into the 'data' table
insert_data_sql = """
    INSERT OR IGNORE INTO data (theme, subreddit, title, content)
    VALUES (?, ?, ?, ?);
"""


delete_rows(conn, 'data', 0, 10)
for i in range(2, len(DATA)):
    # Data to be inserted
    sample_data = ('Sample Theme', DATA['subreddit'][i], DATA['title'][i], DATA['link_url'][i])
    execute_query(conn, insert_data_sql, sample_data)

# Close Connection
conn.close()
