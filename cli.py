import actions


def display_menu():
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Charge Balance")
    print("4. Add Food")
    print("5. Remove Food")
    print("6. Make Reservation")
    print("7. View All Students")
    print("8. View All Foods")
    print("9. View All Reservations")
    print("10. Cancel Reservation")
    print("11. Change Reservation")
    print("12. Exit")


def run():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            # Add Student
            student_id = input("Enter student ID: ")
            major = input("Enter student major: ")
            dob = input("Enter student date of birth (YYYY-MM-DD): ")
            first_name = input("Enter student first name: ")
            last_name = input("Enter student last name: ")
            balance = float(input("Enter student balance: "))
            status = actions.add_student(int(student_id), major, dob, first_name, last_name, balance)
            if status is True:
                print("Student added successfully!")

        elif choice == "2":
            # remove student
            student_id = input("Enter student ID: ")
            actions.remove_student(int(student_id))
            print("Student removed successfully!")

        elif choice == "3":
            # Charge balance
            student_id = input("Enter student ID: ")
            amount = input("Enter amount to charge: ")
            actions.update_balance(int(student_id), amount)
            print("Food added successfully!")

        elif choice == "4":
            # add food
            name = input("Enter food name: ")
            date = input("Enter food date (YYYY-MM-DD): ")
            price = float(input("Enter food price: "))
            inventory = int(input("Enter food inventory: "))
            food_id = actions.add_food(name, date, price, inventory)
            print(f"Food added successfully! Food ID = {food_id}")

        elif choice == "5":
            # remove food
            food_id = input("Enter food ID: ")
            actions.remove_student(int(food_id))
            print("Food removed successfully!")

        elif choice == "6":
            # Make Reservation
            student_id = input("Enter student ID: ")
            food_id = input("Enter food ID: ")
            reservation_id = actions.make_reservation(int(student_id), int(food_id))
            if not reservation_id:
                continue

            print(student_id)
            actions.handle_reservation_changes("1", None, reservation_id, actions.get_current_date())
            print(f"Reservation made successfully! Reservation ID: {reservation_id}")

        elif choice == "7":
            # View All Students
            students = actions.view_all_students()
            for student in students:
                print(student)

        elif choice == "8":
            # View All Foods
            foods = actions.view_all_foods()
            for food in foods:
                print(food)

        elif choice == "9":
            # View All Reservations
            reservations = actions.view_all_reservations()
            for reservation in reservations:
                print(reservation)

        elif choice == "10":
            # Cancel Reservation
            src_reservation_id = input("Enter reservation ID: ")
            actions.handle_reservation_changes("2", src_reservation_id, None, actions.get_current_date())
            print("Reservation canceled successfully!")

        elif choice == "11":
            # change reservation
            student_id = input("Enter student ID: ")
            food_id = input("Enter food ID for new reservation: ")
            source_reservation_id = input("Enter reservation ID to change: ")
            actions.return_price(student_id, source_reservation_id)
            destination_reservation_id = actions.make_reservation(int(student_id), int(food_id))
            actions.handle_reservation_changes("3", source_reservation_id, destination_reservation_id, actions.get_current_date())

        elif choice == "12":
            # Exit the program
            break
