import hashlib

def create_account():
    print("Create a new account:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    with open("user_database.txt", "a") as file:
        file.write(f"{username},{hashed_password}\n")

    print("Account created successfully!\n")

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def login():
    print("Login:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    with open("user_database.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if username == stored_username and hashed_password == stored_password:
                print("Login successful!\n")
                return

    print("Invalid username or password. Please try again.\n")

def main():
    while True:
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
