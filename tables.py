import psycopg2
from psycopg2 import Error


def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Zeinab801224",
            host="localhost",
            port="5432",
            database="food_reservation"
        )
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


def create_tables(connection):
    cursor = connection.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                studentID INTEGER PRIMARY KEY,
                major VARCHAR(50) NOT NULL,
                date_of_birth DATE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                balance DECIMAL(10, 2) DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foods (
                ID SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                date TIMESTAMP NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                inventory INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                ID SERIAL PRIMARY KEY,
                studentID INTEGER REFERENCES students(studentID),
                foodID INTEGER REFERENCES foods(ID),
                status VARCHAR(20) DEFAULT 'On'
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                ID SERIAL PRIMARY KEY,
                srcReservationID INTEGER REFERENCES reservations(ID),
                dstReservationID INTEGER REFERENCES reservations(ID),
                date TIMESTAMP NOT NULL
            )
        ''')

        connection.commit()
        print("Tables created successfully!")
    except (Exception, Error) as error:
        print("Error creating tables:", error)
    finally:
        cursor.close()
