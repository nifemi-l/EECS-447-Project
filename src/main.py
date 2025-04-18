"""
Authors: Holden Vail, Michael Stang, Logan Smith, Blake Carlson, Nifemi Lawal
Class: EECS 447
Assignment: Database Design Project Part 5: Physical Database Design
"""

import getpass
import psycopg2

# Database connection parameters
DB_HOST = "libdb-25co-postgres.cajikaswgj3d.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "LibDB_25Co"
DB_PASSWORD = "null"        # Replace this with the master password

LIBRARY_PASSWORD = "password"

def connect_to_db():
    """Establish a connection to the PostgreSQL DB"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("DB connection successful")
        return conn
    except Exception as e:
        print(f"DB connection failure: {e}")
        return None

def ensure_configured(db_connection):
    """Configure the tables and realtions of the DB"""
    try:
        config_queries = """
        CREATE TABLE IF NOT EXISTS Clients (
            ClientID SERIAL PRIMARY KEY CHECK (ClientID >= 0),
            Name VARCHAR(100) NOT NULL,
            MembershipType ENUM('Regular', 'Student', 'Senior Citizen', 'Other') NOT NULL,
            AccountStatus ENUM('Active', 'Suspended', 'Inactive') NOT NULL,
            EmailAddress VARCHAR(255) UNIQUE NOT NULL,
            PhoneNumber VARCHAR(15) UNIQUE NOT NULL
        );
        """
        cursor = db_connection.cursor()
        cursor.execute(config_queries)
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"exception encountered: {e}")

def verify():
    print("The admin password is required for that action.")
    password_input = getpass.getpass()
    return (password_input == LIBRARY_PASSWORD) # Beautiful security :)

def execute(called_function, params, active_user, admin):
    if admin:
        if verify():
            return called_function(params, active_user)
        else:
            print("Invalid Admin Password. Please try again!")
    else:
        return called_function(params, active_user)

def example_command(params, active_user):
    my_parameter_1 = int(params[0])
    my_parameter_2 = int(params[1])
    print(my_parameter_1 + my_parameter_2)

def main():
    """CLI for interacting with DB"""
    connection  = connect_to_db()
    ensure_configured(connection)

    quit = False
    active_user = ""
    while not quit:
        active_user = input("Please input your Library ID: ")
        if not active_user.isnumeric():
            active_user = ""
            print("Please input a valid Library ID\n")

        while active_user != "":
            input_string = input(">> ")
            command = input_string.split(' ')

            # Insert quote connection

            match command[0].lower():
                case "quit":
                    if verify():
                        quit = True # end program running
                        break
                case "logout":
                    active_user = ""
                case "example":
                    execute(called_function=example_command, params=command[1:], active_user=active_user, admin=False)
                case "admin_example":
                    execute(called_function=example_command, params=command[1:], active_user=active_user, admin=True)
                case _:
                    print("Wow")

main()