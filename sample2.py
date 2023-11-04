import hashlib
import datetime
import mysql.connector

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "hosp_db",
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# SQL Queries
create_users_table_query = """
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    hashed_password VARCHAR(255),
    role VARCHAR(20)
)
"""

create_doctors_table_query = """
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(255),
    specialty VARCHAR(255)
)
"""

create_patients_table_query = """
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255),
    age INT
)
"""

create_appointments_table_query = """
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT,
    patient_id INT,
    appointment_date DATETIME,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
)
"""

cursor.execute(create_users_table_query)
cursor.execute(create_doctors_table_query)
cursor.execute(create_patients_table_query)
cursor.execute(create_appointments_table_query)
connection.commit()

def load_data_from_db(table_name):
    data = {}
    try:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        for row in cursor.fetchall():
            key, *values = row
            data[key] = ','.join(map(str, values))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return data

def save_data_to_db(table_name, data, role='user'):
    try:
        cursor.execute(f"DELETE FROM {table_name}")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data[next(iter(data))].split(',')))
        query = f"INSERT INTO {table_name} ({columns}, role) VALUES ({placeholders}, %s)"

        values_list = [tuple(value.split(',')) + (role,) for value in data.values()]

        for values in values_list:
            print(f"Executing query: {query}")
            print(f"Values: {values}")
            cursor.execute(query, values)

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()

def add_user(username, hashed_password, role='user'):
    users_database[username] = hashed_password
    save_data_to_db("users", users_database, role)

users_database = load_data_from_db("users")
doctors_database = load_data_from_db("doctors")
patients_database = load_data_from_db("patients")
appointments_database = load_data_from_db("appointments")

def admin_signup():
    print("Admin Signup:")
    username = input("Enter your admin username: ")
    password = input("Enter your admin password: ")
    hashed_password = hash_password(password)

    add_user(username, hashed_password, role='admin')

    print("Admin account created successfully!\n")

def patient_signup():
    print("Patient Signup:")
    username = input("Enter your patient username: ")
    password = input("Enter your patient password: ")
    hashed_password = hash_password(password)

    add_user(username, hashed_password, role='patient')

    print("Patient account created successfully!\n")

def create_account():
    print("Create a new account:")
    print("1. Admin Signup")
    print("2. Patient Signup")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        admin_signup()
    elif choice == "2":
        patient_signup()
    else:
        print("Invalid choice. Please enter 1 or 2.\n")

def admin_login():
    print("Admin Login:")
    username = input("Enter your admin username: ")
    password = input("Enter your admin password: ")
    hashed_password = hash_password(password)

    return check_credentials(username, hashed_password, role='admin')

def patient_login():
    print("Patient Login:")
    username = input("Enter your patient username: ")
    password = input("Enter your patient password: ")
    hashed_password = hash_password(password)

    return check_credentials(username, hashed_password, role='patient')

def check_credentials(username, hashed_password, role='user'):
    if username in users_database and hashed_password == users_database[username]:
        print(f"{role.capitalize()} login successful!\n")
        return True, role
    else:
        print(f"Invalid {role} username or password. Please try again.\n")
        return False, None

def login():
    print("Login:")
    print("1. Admin Login")
    print("2. Patient Login")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        return admin_login()
    elif choice == "2":
        return patient_login()
    else:
        print("Invalid choice. Please enter 1 or 2.\n")
        return False, None

# ... (remaining code)

if __name__ == "__main__":
    create_account()

cursor.close()
connection.close()
