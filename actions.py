import psycopg2
from psycopg2 import Error


# Function to connect to the PostgreSQL database
def connect():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="************",
            host="localhost",
            port="5432",
            database="food_reservation"
        )
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


# Function to add a new student to the database with data validation checks
def add_student(student_id, major, date_of_birth, first_name, last_name, balance):
    if student_id <= 0:
        print("Error: Student ID must be a positive integer.")
        return False

    if balance < 0:
        print("Error: Balance must be a non-negative number.")
        return False

    connection = connect()
    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (studentID, major, date_of_birth, first_name, last_name, balance) VALUES (%s, %s, %s, %s, %s, %s)",
            (student_id, major, date_of_birth, first_name, last_name, balance))
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        return False

    cursor.close()
    connection.close()
    return True


# Function to remove a student from the database
def remove_student(student_id):
    connection = connect()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE studentID = %s", (int(student_id),))
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        return False

    cursor.close()
    connection.close()
    return True
