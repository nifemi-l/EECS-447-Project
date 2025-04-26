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
        monthly_fees_report : Displays fees collected by membership type in the last month

        """
        case "member_engagement":
            execute_postgresql(connection, active_user, member_engagement_report)
        case "monthly_fees_report":
            execute_postgresql(connection, active_user, monthly_fees_report)
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
            avg_borro_time_science_fiction  : Average borrowing time for "Science Fiction" books (in days)
            most_pop_author_last_month      : Shows the most borrowed author in the last month
            clients_exceeding_borr_lims     : Lists clients who are currently over their borrowing limits
            """
            print(helper_text)
        case "books_of_2007":
            execute_postgresql(connection, active_user, books_of_2007_query)
        case "availble_horror_digital_media":
            execute_postgresql(connection, active_user, available_horror_digital_media_query)
        case "trans_history_11":
            execute_postgresql(connection, active_user, trans_history_11)
        case "avg_borro_time_science_fiction":
            execute_postgresql(connection, active_user, avg_borro_time_science_fiction)
        case "most_pop_author_last_month":
            execute_postgresql(connection, active_user, most_pop_author_last_month)
        case "clients_exceeding_borr_lims":
            execute_postgresql(connection, active_user, clients_exceeding_borr_lims)
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

# N
avg_borro_time_science_fiction = """
SELECT AVG((t.returned_date::date - t.date_borrowed::date)) AS avg_borrow_days
FROM transaction AS t
JOIN book AS bo ON t.item_id = bo.item_id
WHERE bo.genre = 'Science Fiction'
AND t.returned_date IS NOT NULL;
"""

most_pop_author_last_month = """
SELECT
  bo.author,
  COUNT(*) AS borrow_count
FROM transaction AS t
JOIN book AS bo ON t.item_id = bo.item_id
WHERE t.date_borrowed >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY bo.author
ORDER BY borrow_count DESC
LIMIT 1;
"""

monthly_fees_report = """
-- (assuming $0.25 per day late fee)
SELECT
  c.membership_type,
  SUM(
    GREATEST(
      (t.returned_date::date - t.expected_return_date::date),
      0
    ) * 0.25
  ) AS total_fees_collected
FROM transaction AS t
JOIN client      AS c ON t.client_id = c.client_id
WHERE t.returned_date::date
      BETWEEN CURRENT_DATE - INTERVAL '1 month'
          AND CURRENT_DATE
GROUP BY c.membership_type;
"""

clients_exceeding_borr_lims = """
-- (Regular: 5 items, Student: 10, Senior Citizen: 7, Other: 3)
SELECT
  c.client_id,
  c.name,
  COUNT(*) AS current_borrowed,
  CASE c.membership_type
    WHEN 'Regular'        THEN 5
    WHEN 'Student'        THEN 10
    WHEN 'Senior Citizen' THEN 7
    ELSE 3
  END AS borrow_limit
FROM transaction AS t
JOIN client      AS c ON t.client_id = c.client_id
WHERE t.returned_date IS NULL
GROUP BY c.client_id, c.name, c.membership_type
HAVING COUNT(*) > CASE c.membership_type
                    WHEN 'Regular'        THEN 5
                    WHEN 'Student'        THEN 10
                    WHEN 'Senior Citizen' THEN 7
                    ELSE 3
                  END;
"""