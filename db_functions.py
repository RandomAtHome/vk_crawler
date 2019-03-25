import sqlite3

import config


def connect_to_db():
    """
    Connect to DB specified in config file and create the table we'll be working with
    Table structure: id INTEGER PRIMARY KEY, vk_id INTEGER UNIQUE, first_name TEXT, last_name TEXT
        id: unique id in our DB
        vk_id: id in VK social network
        first_name: first name of user
        last_name: last name of user
    :return: sqlite3.Connection object, representing connection to our DB
    """
    conn = sqlite3.connect(config.DB_NAME)
    conn.execute('''CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY, vk_id INTEGER UNIQUE, first_name TEXT, last_name TEXT
        )''')
    conn.commit()
    return conn


def update_db(cursor: sqlite3.Cursor, users: map):
    """
    Get cursor pointing to DB, iterator of prepared user data and update the DB
    :param cursor: cursor pointing to DB
    :param users: vk user objects mapped to special dicts
    """
    for user in users:
        cursor.execute('''UPDATE Users SET first_name=:first_name, last_name=:last_name
            WHERE vk_id = :vk_id;''', user)
        cursor.execute('''INSERT OR IGNORE INTO Users(vk_id, first_name, last_name)
            VALUES (:vk_id, :first_name, :last_name)''', user)
    cursor.connection.commit()
