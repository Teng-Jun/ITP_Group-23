import mysql.connector
from mysql.connector import Error

def test_database_connection():
    try:
        connection = mysql.connector.connect(
            host='13.76.25.253',
            user='phpmyadmin',
            password='xji],x4~hSTBCqd',
            database='itp'
        )

        if connection.is_connected():
            print("Connection to the database was successful!")
            
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("Tables in the database:", tables)

    except Error as e:
        print(f"Error while connecting to the database: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    test_database_connection()

