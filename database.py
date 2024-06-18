import sqlite3
import atexit
import random
from datetime import datetime, timedelta

def close_connection_cb(conn):
    conn.close()
    
class DB:
    def __init__(self):
        self.connect()


    def connect(self):
        self.connection = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        atexit.register(close_connection_cb, self.connection)
    
    def add_user(self, user_id: int, take_not: int, username: str):
        res = self.cursor.execute(
            'SELECT * FROM users_main WHERE user_id = ?',
            (user_id,)
        ).fetchone()
        if res is None:
            #УНИКАЛЬНЫЙ ЮЗЕР
            self.cursor.execute(
                'INSERT INTO users_main (user_id, is_take_not, datetime, username) VALUES (?, ?, ?, ?)', (user_id, take_not, datetime.now(), username)
            )
            self.cursor.connection.commit()
            return True
        else:
            return False
    def get_statistics(self, time: str):
        today = datetime.now().date()
        if time == 'today':
            res = self.cursor.execute(
                'SELECT COUNT(*) FROM users_main WHERE DATE(datetime) = ?',
                (today,)
            ).fetchone()
            return res[0]
        if time == 'yesterday':
            yesterday = today - timedelta(days=1)
            res = self.cursor.execute(
                'SELECT COUNT(*) FROM users_main WHERE DATE(datetime) = ?',
                (yesterday,)
            ).fetchone()
            return res[0]
        if time == 'week':
            this_week = today - timedelta(days=today.weekday())
            res = self.cursor.execute(
                'SELECT COUNT(*) FROM users_main WHERE DATE(datetime) = ?',
                (this_week,)
            ).fetchone()
            return res[0]
        if time == 'all':
            res = self.cursor.execute(
                'SELECT COUNT(*) FROM users_main'
            ).fetchone()
            return res[0]
    def get_all_users(self):
        res = self.cursor.execute(
            'SELECT * FROM users_main'
        ).fetchall()
        return res
    def is_take_not(self, user_id: int):
        res = self.cursor.execute(
            'SELECT is_take_not FROM users_main WHERE user_id = ?',
            (user_id,)
        ).fetchone()
        return res[0]
    
    