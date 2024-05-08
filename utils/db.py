import mysql.connector

class DatabaseManager(object):

    @staticmethod
    def get_connection():
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
        )
        return connection

if __name__=='__main__':
    connection = DatabaseManager.get_connection()