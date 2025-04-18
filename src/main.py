"""
Authors: Holden Vail, Michael Stang, Logan Smith, Blake Carlson, Nifemi Lawal
Class: EECS 447
Assignment: Database Design Project Part 5: Physical Database Design
"""

import getpass
import psycopg2
import sqlparse
import cli_commands as cli

# Database connection parameters
DB_HOST = "libdb-25co-postgres.cajikaswgj3d.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "LibDB_25Co"
DB_PASSWORD = "hnmbl.EECS447!lib_DB_proj?"        # Replace this with the master password

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

def is_correctly_configured(db_connection):
    """Verify the database schema using the libraryDDL.sql file."""
    ddl_path = "src/libraryDDL.sql"

    try:
        with open(ddl_path, 'r') as ddl_file:
            ddl_content = ddl_file.read()

        # Remove comments from the SQL file
        ddl_content = sqlparse.format(ddl_content, strip_comments=True)

        # Parse the SQL statements
        statements = sqlparse.split(ddl_content)

        cursor = db_connection.cursor()

        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"Schema verification failed for statement: {statement}\n{e}")
                    return False

        print("Database schema matches expectation")
        cursor.close()
        return True

    except FileNotFoundError:
        print("DDL file not found")
        return False
    except Exception as e:
        print(f"Exception encountered: {e}")
        return False

def verify():
    print("The admin password is required for that action.")
    password_input = getpass.getpass()
    return (password_input == LIBRARY_PASSWORD) # Beautiful security :)

def execute(active_user, called_function, admin=False, args=None):
    if admin:
        if verify():
            called_function(active_user, args)
        else:
            print("Invalid Admin Password. Please try again!")
    else:
        called_function(active_user, args)

def main():
    """CLI for interacting with DB"""
    connection = connect_to_db()
    if not is_correctly_configured(connection):
        raise Exception("Database is not correctly configured!")

    quit = False
    active_user = ""
    while not quit:
        active_user = input("Please input your Client ID: ")
        if not active_user.isnumeric():
            active_user = ""
            print("Please input a valid Client ID\n")
            continue

        while active_user != "":
            input_string = input(">> ")
            command = input_string.split(' ')

            match command[0].lower():
                case "quit":
                    if verify():
                        quit = True
                        break
                case "logout":
                    active_user = ""
                case "clear":
                    execute(active_user, cli.clear)
                case "help":
                    execute(active_user, cli.library_help)
                case "":
                    continue
                case _:
                    print(f"No command found for: {command[0]}")

main()