import hashlib
import datetime

# File paths for data storage
users_file = "users.txt"
doctors_file = "doctors.txt"
patients_file = "patients.txt"
appointments_file = "appointments.txt"

# Load existing data from files
users_database = {}
doctors_database = {}
patients_database = {}
appointments_database = {}


def load_data_from_file(file_path):
    data = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                key, *values = line.strip().split(',')
                data[key] = ','.join(values)
    except FileNotFoundError:
        pass
    return data


def save_data_to_file(file_path, data):
    with open(file_path, "w") as file:
        for key, value in data.items():
            file.write(f"{key},{value}\n")


# Load existing data from files at the beginning
users_database = load_data_from_file(users_file)
doctors_database = {int(k): v for k, v in load_data_from_file(doctors_file).items()}
patients_database = {int(k): v for k, v in load_data_from_file(patients_file).items()}
appointments_database = load_data_from_file(appointments_file)


def create_account():
    print("Create a new account:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    # Store the user information in the database
    users_database[username] = hashed_password
    save_data_to_file(users_file, users_database)

    print("Account created successfully!\n")


def hash_password(password):
    # Use a secure hashing algorithm, like SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def login():
    print("Login:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    # Check if the user exists and the password is correct
    if username in users_database and hashed_password == users_database[username]:
        print("Login successful!\n")
        return True, users_database[username]
    else:
        print("Invalid username or password. Please try again.\n")
        return False, None


def add_doctor():
    print("Add a new doctor:")
    doctor_name = input("Enter doctor's name: ")
    specialty = input("Enter doctor's specialty: ")

    doctor_id = len(doctors_database) + 1
    doctors_database[doctor_id] = f"{doctor_name},{specialty}"
    save_data_to_file(doctors_file, doctors_database)

    print(f"Doctor {doctor_name} added successfully with ID {doctor_id}\n")


def add_patient():
    print("Add a new patient:")
    patient_name = input("Enter patient's name: ")
    age = input("Enter patient's age: ")

    patient_id = len(patients_database) + 1
    patients_database[patient_id] = f"{patient_name},{age}"
    save_data_to_file(patients_file, patients_database)

    print(f"Patient {patient_name} added successfully with ID {patient_id}\n")


def schedule_appointment():
    print("Schedule a new appointment:")
    doctor_id = input("Enter doctor's ID: ")
    patient_id = input("Enter patient's ID: ")

    doctor_id = int(doctor_id)
    patient_id = int(patient_id)

    if doctor_id in doctors_database and patient_id in patients_database:
        appointment_id = len(appointments_database) + 1
        date_time = input("Enter date and time (YYYY-MM-DD HH:MM): ")
        try:
            appointment_date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            appointments_database[appointment_id] = f"{doctor_id},{patient_id},{appointment_date}"
            save_data_to_file(appointments_file, appointments_database)

            print(f"Appointment scheduled successfully with ID {appointment_id}\n")
        except ValueError:
            print("Invalid date and time format. Please use YYYY-MM-DD HH:MM.\n")
    else:
        print("Invalid doctor's ID or patient's ID. Please check and try again.\n")


def hospital_management_system():
    while True:
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            create_account()
        elif choice == "2":
            login_status, user_role = login()
            if login_status:
                if user_role == 'admin':
                    admin_menu()
                elif user_role == 'user':
                    user_menu()
                elif user_role == 'doctor':
                    doctor_menu()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")


def admin_menu():
    while True:
        print("Admin Menu:")
        print("1. Add Doctor")
        print("2. Add Patient")
        print("3. Schedule Appointment")
        print("4. Logout")

        admin_choice = input("Enter your choice (1/2/3/4): ")

        if admin_choice == "1":
            add_doctor()
        elif admin_choice == "2":
            add_patient()
        elif admin_choice == "3":
            schedule_appointment()
        elif admin_choice == "4":
            print("Logging out.\n")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.\n")


def user_menu():
    print("User Menu:")
    # Add user-specific functionalities here
    print("Logout\n")


def doctor_menu():
    print("Doctor Menu:")
    # Add doctor-specific functionalities here
    print("Logout\n")


if __name__ == "__main__":
    # hospital_management_system()
    admin_menu()