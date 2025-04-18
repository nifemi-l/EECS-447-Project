import os

# Every function must accept connection, active_user and args as parameters. args may be None type

def library_help(connection, active_user, args):
    """Displays the helper text"""
    helper_text = """
    help    : show this helper text
    logout  : clear the active user
    quit    : close the session and exit
    clear   : clear the screen
    execpg  : execute an arbitrary PostgreSQL command (requires admin privileges)
    """
    print(helper_text)

def clear(connection, active_user, args):
    """Clears the screen"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def execute_postgresql(connection, active_user, input_string):
    """
    Execute an arbitrary postgres command. Requires admin privileges.
    """

    command = input_string.split(' ')
    if len(command) <= 1:
        print("No postgres command provided.")
        return
    else:
        command = ' '.join(command[1:])

    try:
        cursor = connection.cursor()

        # Execute the SQL command
        cursor.execute(command)
        connection.commit()

        # Fetch and display results if it's a SELECT query
        if command.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for row in results:
                print(row)

        print("SQL command executed successfully.")
        cursor.close()
    except Exception as e:
        print(f"Error executing SQL command: {e}")