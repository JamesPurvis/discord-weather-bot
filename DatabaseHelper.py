import mysql.connector


class DatabaseHelper:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to the database.")
        except mysql.connector.Error as error:
            print("Error connecting to the database:", error)

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            results = cursor.fetchone()
            self.connection.commit()
            print("Query executed successfully.")
            return results

        except mysql.connector.Error as error:
            print("Error executing query:", error)
        finally:
            cursor.close()

