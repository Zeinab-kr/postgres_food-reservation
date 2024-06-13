import psycopg2
from psycopg2 import Error


def connect_to_db():
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
