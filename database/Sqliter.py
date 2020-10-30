import sqlite3
import os.path


class Sqliter(object):
    """класс взаимодействия с БД"""

    def __init__(self, database_name: str = "db"):
        # подключение к БД
        self.connection = sqlite3.connect(database_name)
        # курсор которым будем водить по данным
        self.cursor = self.connection.cursor()
        self.database_name = database_name

    def get_info_all_users(self) -> list:
        '''получение информации всех пользователей'''
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()

    def get_info_user(self, user_id: str) -> list:
        '''получение информации об одном пользователе'''
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE user_id = ?", user_id).fetchall()

    def add_user_info(self, user_id: str, learn: str, sleep: bool, sport: bool, thanks: str) -> list:
        '''добавление информации пользователя'''
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id , learn , sleep , sport ,mentors) " +
                                       "VALUES (?,?,?,?,?)", (user_id, learn, sleep, sport, thanks)).fetchall()

    def init_database(self):
        '''init to database'''
        with open("database\\" + self.database_name, "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()

    def check_init_database(self):
        '''check exists database'''
        if os.path.exists(self.database_name):
            pass
        else:
            self.init_database()

    def truncate_table(self):
        '''Truncate table from DB'''
        with self.connection:
            self.cursor.execute('DELETE FROM subscriptions')
