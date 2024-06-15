import psycopg2
from psycopg2 import Error


def get_current_date():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    return current_date

    
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


# Function to add a new food item to the database with data validation checks
def add_food(name, date, price, inventory):
    if not isinstance(price, (int, float)) or price < 0:
        print("Error: Price must be a non-negative number.")
        return False

    if not isinstance(inventory, int) or inventory < 0:
        print("Error: Inventory must be a non-negative integer.")
        return False

    connection = connect()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO foods (name, date, price, inventory) VALUES (%s, %s, %s, %s) RETURNING ID",
                       (name, date, price, inventory))
        food_id = cursor.fetchone()[0]
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        return False

    cursor.close()
    connection.close()
    return food_id


# Function to remove a food item from the database
def remove_food(food_id):
    connection = connect()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM foods WHERE ID = %s", (food_id,))
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        return False

    cursor.close()
    connection.close()
    return True


# Function to make a food reservation with data validation checks
def make_reservation(student_id, food_id):
    if student_id <= 0 or food_id <= 0:
        print("Error: Student ID and Food ID must be positive integers.")
        return False

    connection = connect()
    if connection is None:
        return False

    cursor = connection.cursor()

    cursor.execute("SELECT price FROM foods WHERE ID = %s", (food_id,))
    price = cursor.fetchone()[0]
    connection.commit()
    print(student_id)
    print(price)
    cursor.execute("SELECT balance FROM students WHERE studentID = %s", (student_id,))
    balance = cursor.fetchone()[0]
    print(balance)
    if balance - price < 0:
        print("No balance!")
        return False

    cursor.execute("UPDATE foods SET inventory = inventory - 1 WHERE ID = %s", (food_id,))
    cursor.execute("INSERT INTO reservations (studentID, foodID) VALUES (%s, %s) RETURNING ID", (student_id, food_id))
    reservation_id = cursor.fetchone()[0]
    connection.commit()
    
    update_balance(student_id, 0 - price)

    cursor.close()
    connection.close()

    return reservation_id


# Function to handle changes in reservations
def handle_reservation_changes(choice, source_reservation_id, destination_reservation_id, date):
    connection = connect()
    if connection is None:
        return False

    cursor = connection.cursor()

    # making new reservation
    if choice == "1":
        cursor.execute("INSERT INTO transactions (srcReservationID, dstReservationID, date) VALUES (NULL, %s, %s)",
                       (destination_reservation_id, date,))

        # Case 2: Cancelling a  reservation
    elif choice == "2":
        cursor.execute("INSERT INTO transactions (srcReservationID, dstReservationID, date) VALUES (%s, NULL, %s)",
                       (source_reservation_id, date,))
        cursor.execute("UPDATE reservations SET status = 'cancelled' WHERE ID = %s", (source_reservation_id,))

        # Case 3: Changing the reservation
    elif choice == "3":
        cursor.execute("INSERT INTO transactions (srcReservationID, dstReservationID, date) VALUES (%s, %s, %s)",
                       (source_reservation_id, destination_reservation_id, date))
        cursor.execute("UPDATE reservations SET status = 'cancelled' WHERE ID = %s", (source_reservation_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return True


def return_price(studentID, source_reservation_id):
    connection = connect()
    if connection is None:
        return False

    cursor = connection.cursor()
    foodID_old = cursor.execute("SELECT foodID FROM reservations WHERE ID = %s",
                                           (int(source_reservation_id),))
    price_old = cursor.execute("SELECT price FROM foods WHERE ID = %s", (foodID_old,))
    print(foodID_old)
    print(source_reservation_id)
    print(price_old)
    cursor.execute("UPDATE students SET balance = balance + %s WHERE studentID = %s", (price_old, studentID))

    connection.commit()
    cursor.close()
    connection.close()
    return True


# Function to update the balance of a student
def update_balance(studentID, amount):
    connection = connect()
    if connection is None:
        return False

    cursor = connection.cursor()
    cursor.execute("UPDATE students SET balance = balance + %s WHERE studentID = %s", (amount, int(studentID)))
    connection.commit()

    cursor.close()
    connection.close()

    return True


# Function to view all students in the database
def view_all_students():
    connection = connect()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return students


# Function to view all foods in the database
def view_all_foods():
    connection = connect()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM foods")
    foods = cursor.fetchall()

    cursor.close()
    connection.close()

    return foods


# Function to view all reservations in the database
def view_all_reservations():
    connection = connect()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reservations")
    reservations = cursor.fetchall()

    cursor.close()
    connection.close()

    return reservations
