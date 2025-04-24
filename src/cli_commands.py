import os

# Every function must accept connection, active_user and args as parameters. args may be None type

def library_help(connection, active_user, input_string):
    """Displays the helper text"""
    helper_text = """
    help    : show this helper text
    logout  : clear the active user
    quit    : close the session and exit
    clear   : clear the screen
    execute  : execute an arbitrary PostgreSQL command (requires admin privileges)
    """
    print(helper_text)

def clear(connection, active_user, input_string):
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

def generate_report(connection, active_user, input_string):
    command = input_string.split(' ')
    if len(command) <= 1:
        print("Request a report or help to see options")
        return
    
    match command[1]:
        case "help":
            helper_text = """
        Options:
        member_engagement   : Generates and displays a member engagement report
        """
        case "member_engagement":
            execute_postgresql(connection, active_user, member_engagement_report)
        case _:
            print(f"No report is available for {command[1]}") 

def query(connection, active_user, input_string):
    command = input_string.split(' ')
    if len(command) <= 1:
        print("Request a query or help to see options")
        return
    
    match command[1]:
        case "help":
            helper_text = """
        Options:
        books_of_2007                   : Gets all the books published in 2007
        availble_horror_digital_media   : Gets all digital media items that are available in the horror genre
        trans_history_11                : Gets all transactions involving item ID 11
        """
        case "books_of_2007":
            execute_postgresql(connection, active_user, books_of_2007_query)
        case "availble_horror_digital_media":
            execute_postgresql(connection, active_user, available_horror_digital_media_query)
        case "trans_history_11":
            execute_postgresql(connection, active_user, trans_history_11)
        case _:
            print(f"No query is available for {command[1]}") 

member_engagement_report = """
SELECT c.client_id, c.name, COUNT(t.transaction_id) AS total_transactions
FROM Client c
LEFT JOIN Transaction t ON c.client_id = t.client_id
GROUP BY c.client_id, c.name
ORDER BY total_transactions DESC;
"""

books_of_2007_query = """
SELECT title, author, publication_year
FROM Book
WHERE publication_year = 2007;
"""

available_horror_digital_media_query = """
SELECT title, author, genre, availability_status
FROM Digital_Media
WHERE genre = 'Horror' AND availability_status = 'Available';
"""

trans_history_11 = """
SELECT transaction_id, client_id, date_borrowed, expected_return_date, returned_date
FROM Transaction
WHERE item_id = 11;
"""
