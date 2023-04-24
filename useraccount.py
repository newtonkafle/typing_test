import sqlite3


class Account:
    def __init__(self) -> None:
        self.db_name = "user.db"
        self.user_name = None
        self.avatar = None
        self.average_wpm = 0
        self.average_accuracy = 0
        self.curr_lesson = 1
        self.db_init()

    # methods to add account
    def add_account(self, user_name, avatar):
        self.user_name = user_name
        self.avatar = avatar

        statement = "INSERT INTO users (username, avatar, average_wpm, average_accuracy, current_lesson) values(?, ?, ?, ?, ?)"
        query_params = (
            self.user_name,
            self.avatar,
            self.average_wpm,
            self.average_accuracy,
            self.curr_lesson,
        )

        self.db_insert(statement, query_params)

        # connection to the data base

    def load_account():
        pass
        # it needs to load the all the user info before loading the session

    def db_init(self):
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        # create user_table
        try:
            users = "Create Table users(username Text, avatar BLOB, average_wpm INT, average_accuracy INT, current_lesson INT)"
            cursor.execute(users)
            db.commit()
        except:
            print("table exists already")
        finally:
            db.close()

    def db_insert(self, statement, params):
        # necessary measure for the security is need to be performed
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(statement, params)
        conn.commit()
        conn.close()
