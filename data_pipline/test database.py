
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        # Establishing the connection to the database
        connection = mysql.connector.connect(
            host='crypto-matter.c5eq66ogk1mf.eu-central-1.rds.amazonaws.com',
            database='Crypto',
            user='Jing',  # replace with your actual first name
            password='Crypto12!'
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_info)

            # Creating a cursor object using the cursor() method
            cursor = connection.cursor()

            # Executing a simple query
            cursor.execute("SELECT DATABASE();")

            # Fetch the result
            record = cursor.fetchone()
            print("You're connected to the database:", record)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Call the function
connect_to_database()
