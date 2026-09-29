import billing
from db import DB
import email

# User interface layer
# Here we interact with the user to get input
# Any work is delegated to the business logic layer


def new_user_ui(db: DB):
    username = input("Enter username to create: ")
    try:
        new_user(db, username)
        print(f"User '{username}' created.")
    except DB.UniqueConstraintError as e:
        print("Sorry, that username is already taken. Want to try again?")


def remove_user_ui(db: DB):
    username = input("Enter username to delete: ")
    db.delete_user(username)


# Business logic layer
# Here we do "business logic"
# This layer does not interact with the user directly
# We delegate actual work to other low-level layers
# Like: db layer, billing layer, email layer, etc.


def new_user(db: DB, username: str):
    # Call the billing layer
    billing.charge_new_user(username)
    # Call the db layer
    try:
        db.insert(username)
    except DB.UniqueConstraintError:
        db.insert(username + "_1")
    # call the email layer
    email.send_welcome_email(username)

def remove_user(db, username):
    return db.delete(username)


def menu():
    while True:
        print("""User Management Menu:
    1. Create User
    2. Delete User
    3. List Users""")
        choice = input("Enter your choice: ")
        if choice == "1":
            new_user_ui(db)
        elif choice == "2":
            remove_user_ui(db)
        elif choice == "3":
            users = db.list_users()
            print("Current users:\n-", "\n- ".join(users))
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    db = DB("db://mock-connection-string")
    menu()
