import sqlite3
from sqlite3 import Error
import sys
from paths import PATH_TO_REDDIT_API, PATH_TO_SQLITE
sys.path.append(PATH_TO_REDDIT_API)
sys.path.append(PATH_TO_SQLITE)
from redditConn import getData
from redditComments import get_comments
from selectTheme import get_themes

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

def refresh_data():
    conn = create_connection('sqlite/allR.db')
    insert_data_sql = """
    INSERT OR IGNORE INTO data (post_id, theme, subreddit, title, content)
    VALUES (?, ?, ?, ?, ?);
    """
    #TODO HERE################
    
    themes = get_themes()
    if themes != None:
        for key, values in themes.items():
            print(values)
            for value in values:
                DATA = getData(value)
    ##########################
                #delete_rows(conn, 'data', 0, 10)
                for i in range(2, len(DATA)):
                    # Data to be inserted
                    data = (DATA['name'][i][3:], key, DATA['subreddit'][i], DATA['title'][i], DATA['link_url'][i])
                    execute_query(conn, insert_data_sql, data)

def insert_comments(post_id, comment_limit):
    comments = get_comments(post_id, comment_limit)
    conn = create_connection('sqlite/allR.db')
    insert_data_sql = """
    INSERT OR IGNORE INTO comments (post_id, content)
    VALUES (?, ?);
    """
    delete_rows(conn, 'comments', 0, comment_limit)
    for comment in comments:
        # Data to be inserted
        data = (post_id, comment)
        execute_query(conn, insert_data_sql, data)

def insert_theme(theme, subreddits):
    conn = create_connection('sqlite/allR.db')
    insert_data_sql = """
    INSERT OR IGNORE INTO themeSubs (theme, subreddits)
    VALUES (?, ?);
    """
    for subreddit in subreddits:
        print(subreddit)
        # Data to be inserted
        data = (theme, subreddit)
        execute_query(conn, insert_data_sql, data)

# SQL command to drop the table
'''table_name = 'themeSubs'
drop_table_sql = f'DROP TABLE IF EXISTS {table_name};'
execute_query(conn, drop_table_sql)'''

# Create data table
create_data_table = """
CREATE TABLE IF NOT EXISTS data (
    post_id TEXT PRIMARY KEY NOT NULL,
    theme TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
"""
execute_query(conn, create_data_table)  

# Create comment table
create_comment_table = """
CREATE TABLE IF NOT EXISTS comments (
    post_id TEXT NOT NULL,
    content TEXT NOT NULL
);
"""
execute_query(conn, create_comment_table)  

# Create theme table
create_theme_table = """
    CREATE TABLE IF NOT EXISTS themeSubs (
        theme TEXT NOT NULL,
        subreddits TEXT NOT NULL
    );
    """
execute_query(conn, create_theme_table)


# Define the SQL command to insert data into the 'data' table
insert_data_sql = """
    INSERT OR IGNORE INTO data (theme, subreddit, title, content)
    VALUES (?, ?, ?, ?);
"""


# Close Connection
conn.close()
