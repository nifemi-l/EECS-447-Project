import os

# Every function must accept connection, active_user and args as parameters. args may be None type

def library_help(connection, active_user, input_string):
    """Displays the helper text"""
    helper_text = """
    help    : show this helper text
    logout  : clear the active user
    quit    : close the session and exit
    clear   : clear the screen
    execute : execute an arbitrary PostgreSQL command (requires admin privileges)
    query   : executes pre-baked queries. Use "query help" to see options
    generate_report : generates pre-baked reports. Use "generate help" to see options
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

    command = input_string

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
            print(helper_text)
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
            available_horror_digital_media  : Gets all digital media items that are available in the horror genre
            trans_history_11                : Gets all transactions involving item ID 11
            avg_borro_time_science_fiction  : Average borrowing time for "Science Fiction" books (in days)
            most_pop_author_last_month      : Shows the most borrowed author in the last month
            clients_exceeding_borr_lims     : Lists clients who are currently over their borrowing limits
            check_client_42                 : Checks the status and information of client 42
            books_by_stephen_king           : Shows all books by Stephen King
            owed_fines_per_client           : Shows the fines owed by each client
            book_mystery_availability       : Lists available books in the 'Mystery' genre
            frequent_borrower_thriller      : Top 5 clients who borrowed the most thrillers this year
            books_due_soon                  : Books that are due within the next 7 days
            members_with_overdue_books      : Clients who currently have overdue books
            frequent_borrowed_items_by_type : Most borrowed book titles per membership type
            never_late_clients              : Clients who have never returned an item late
            avg_loan_duration               : Average loan duration (in days)
            monthly_summary_report          : Summary of this month's loans, fees, and popular item
            borrowing_history_report        : Full borrowing history with late fee calculations
            currently_checked_out           : Items currently checked out (unreturned)
            item_availability_and_history   : Full item history with current status and late fees
            overdue_items_report            : Report on all currently overdue items and fees
            revenue_summary                 : Total outstanding fees by membership and item category
            monthly_fees_report             : Fees collected for returned items within the last month
            """
            
            print(helper_text)
        case "books_of_2007":
            execute_postgresql(connection, active_user, books_of_2007)
        case "trans_history_11":
            execute_postgresql(connection, active_user, trans_history_11)
        case "avg_borro_time_science_fiction":
            execute_postgresql(connection, active_user, avg_borro_time_science_fiction)
        case "most_pop_author_last_month":
            execute_postgresql(connection, active_user, most_pop_author_last_month)
        case "clients_exceeding_borr_lims":
            execute_postgresql(connection, active_user, clients_exceeding_borr_lims)
        case "check_client_42":
            execute_postgresql(connection, active_user, check_client_42)
        case "owed_fines_per_client":
            execute_postgresql(connection, active_user, owed_fines_per_client)
        case "books_by_stephen_king":
            execute_postgresql(connection, active_user, books_by_stephen_king)
        case "book_mystery_availability":
            execute_postgresql(connection, active_user, book_mystery_availability)
        case "frequent_borrower_romance":
            execute_postgresql(connection, active_user, frequent_borrower_romance)
        case "books_due_soon":
            execute_postgresql(connection, active_user, books_due_soon)
        case "members_with_overdue_books":
            execute_postgresql(connection, active_user, members_with_overdue_books)
        case "frequent_borrowed_items_by_type":
            execute_postgresql(connection, active_user, frequent_borrowed_items_by_type)
        case "never_late_clients":
            execute_postgresql(connection, active_user, never_late_clients)
        case "avg_loan_duration":
            execute_postgresql(connection, active_user, avg_loan_duration)
        case "monthly_summary_report":
            execute_postgresql(connection, active_user, monthly_summary_report)           
        case "borrowing_history_report":
            execute_postgresql(connection, active_user, borrowing_history_report)
        case "currently_checked_out":
            execute_postgresql(connection, active_user, currently_checked_out)
        case "item_availability_and_history":
            execute_postgresql(connection, active_user, item_availability_and_history)
        case "overdue_items_report":
            execute_postgresql(connection, active_user, overdue_items_report)
        case "revenue_summary":
            execute_postgresql(connection, active_user, revenue_summary)
        case "monthly_fees_report":
            execute_postgresql(connection, active_user, monthly_fees_report)
        case _:
            print(f"No query is available for {command[1]}")

member_engagement_report = """
SELECT DISTINCT c.client_id, c.name, COUNT(t.transaction_id) AS total_transactions
FROM Client c
LEFT JOIN Transaction t ON c.client_id = t.client_id
GROUP BY c.client_id, c.name
ORDER BY total_transactions DESC;
"""

trans_history_11 = """
SELECT transaction_id, client_id, date_borrowed, expected_return_date, returned_date
FROM Transaction
WHERE item_id = 11;
"""

# Nifemi

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

# Just fees collected in the last month (excludes not returned/paid)
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

# Holden

books_by_stephen_king = """
SELECT *
FROM Book
WHERE author = 'Stephen King';
"""

books_of_2007 = """
SELECT *
FROM Book
WHERE publication_year = 2007;
"""

check_client_42 = """
SELECT *
FROM Client
WHERE client_id = 42;
"""

owed_fines_per_client = """
SELECT
  c.client_id,
  c.name,
  SUM(
    GREATEST(
      (t.returned_date::date - t.expected_return_date::date),
      0
    ) * 0.25
  ) AS total_owed
FROM transaction AS t
JOIN client AS c ON t.client_id = c.client_id
WHERE t.returned_date IS NOT NULL -- Only consider returned items
  AND t.returned_date > t.expected_return_date
GROUP BY c.client_id, c.name
HAVING SUM(GREATEST((t.returned_date::date - t.expected_return_date::date), 0) * 0.25) > 0;
"""

# Michael

book_mystery_availability = """
SELECT
    b.title,
    b.item_id
FROM media_item AS m
JOIN book AS b ON m.item_id = b.item_id
WHERE b.genre = 'Mystery' AND m.availability_status = 'Available';
"""

frequent_borrower_romance = """
SELECT
    c.client_id,
    c.name,
    COUNT(*) AS romance_borrow_count
FROM transaction AS t
JOIN media_item AS m ON t.item_id = m.item_id
JOIN book AS b ON m.item_id = b.item_id
JOIN client AS c ON t.client_id = c.client_id
WHERE b.genre = 'Romance' AND (t.date_borrowed >= CURRENT_DATE - INTERVAL '1 year')
GROUP BY c.client_id, c.name
ORDER BY romance_borrow_count DESC;
"""

books_due_soon = """
SELECT
    b.title,
    b.item_id,
    c.name,
    t.expected_return_date
FROM transaction AS t
JOIN media_item AS m ON t.item_id = m.item_id
JOIN book AS b ON m.item_id = b.item_id
JOIN client AS c ON t.client_id = c.client_id
WHERE (t.expected_return_date >= CURRENT_DATE) AND (t.expected_return_date <= CURRENT_DATE + INTERVAL '7 days') AND t.returned_date IS NULL
ORDER BY t.expected_return_date ASC;
"""

members_with_overdue_books = """
SELECT
    c.client_id,
    c.name,
    b.title,
    t.expected_return_date
FROM transaction AS t
JOIN media_item AS m ON t.item_id = m.item_id
JOIN book AS b ON m.item_id = b.item_id
JOIN client AS c ON t.client_id = c.client_id
WHERE t.expected_return_date < CURRENT_DATE AND t.returned_date IS NULL
ORDER BY c.name, t.expected_return_date;
"""

# Logan

frequent_borrowed_items_by_type = """
SELECT
    c.membership_type,
    b.title,
    COUNT(*) AS borrow_count
FROM transaction AS t
JOIN media_item AS m ON t.item_id = m.item_id
JOIN book AS b ON m.item_id = b.item_id
JOIN client AS c ON t.client_id = c.client_id
GROUP BY c.membership_type, b.title
ORDER BY c.membership_type, borrow_count DESC;
"""

never_late_clients = """
SELECT DISTINCT
    c.client_id,
    c.name
FROM client AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM transaction AS t
    WHERE t.client_id = c.client_id
      AND t.returned_date > t.expected_return_date
);
"""

avg_loan_duration = """
SELECT
    AVG(t.returned_date::date - t.date_borrowed::date) AS avg_loan_duration_days
FROM transaction AS t
WHERE t.returned_date IS NOT NULL;
"""

monthly_summary_report = """
SELECT
  (SELECT COUNT(*)
   FROM transaction
   WHERE date_borrowed >= date_trunc('month', CURRENT_DATE)) AS total_items_loaned,

  (SELECT SUM(
      GREATEST(
        (returned_date::date - expected_return_date::date),
        0
      ) * 0.25)
   FROM transaction
   WHERE returned_date >= date_trunc('month', CURRENT_DATE)) AS total_fees_collected,

  (SELECT b.title
   FROM transaction AS t
   JOIN media_item AS m ON t.item_id = m.item_id
   JOIN book AS b ON m.item_id = b.item_id
   WHERE t.date_borrowed >= date_trunc('month', CURRENT_DATE)
   GROUP BY b.title
   ORDER BY COUNT(*) DESC
   LIMIT 1) AS most_popular_item;
"""

# Blake

borrowing_history_report = """
SELECT
    c.client_id,
    c.name,
    t.transaction_id,
    mi.item_id,
    b.title AS book_title,
    dm.title AS digital_media_title,
    mg.title AS magazine_title,
    t.date_borrowed,
    t.expected_return_date,
    t.returned_date,
    CASE 
        WHEN t.returned_date IS NULL AND CURRENT_DATE > t.expected_return_date
        THEN EXTRACT(DAY FROM (CURRENT_DATE - t.expected_return_date)) * 0.25
        ELSE 0
    END AS late_fee
FROM Client c
JOIN Transaction t ON c.client_id = t.client_id
JOIN Media_Item mi ON t.item_id = mi.item_id
LEFT JOIN Book b ON mi.item_id = b.item_id
LEFT JOIN Digital_Media dm ON mi.item_id = dm.item_id
LEFT JOIN Magazine mg ON mi.item_id = mg.item_id
ORDER BY c.client_id, t.date_borrowed DESC;
"""

currently_checked_out = """
SELECT DISTINCT
    c.client_id,
    c.name,
    t.transaction_id,
    mi.item_id,
    b.title AS book_title,
    dm.title AS digital_media_title,
    mg.title AS magazine_title,
    t.date_borrowed,
    t.expected_return_date,
    t.returned_date,
    CASE 
        WHEN t.returned_date IS NULL AND CURRENT_DATE > t.expected_return_date
        THEN EXTRACT(DAY FROM (CURRENT_DATE - t.expected_return_date)) * 0.25
        ELSE 0
    END AS late_fee
FROM Client c
JOIN Transaction t ON c.client_id = t.client_id
JOIN Media_Item mi ON t.item_id = mi.item_id
LEFT JOIN Book b ON mi.item_id = b.item_id
LEFT JOIN Digital_Media dm ON mi.item_id = dm.item_id
LEFT JOIN Magazine mg ON mi.item_id = mg.item_id
WHERE t.returned_date IS NULL
ORDER BY c.client_id, t.date_borrowed DESC;
"""

item_availability_and_history = """
SELECT
    c.client_id,
    c.name,
    t.transaction_id,
    mi.item_id,
    b.title AS book_title,
    dm.title AS digital_media_title,
    mg.title AS magazine_title,
    t.date_borrowed,
    t.expected_return_date,
    t.returned_date,
    CASE 
        WHEN t.returned_date IS NULL AND CURRENT_DATE > t.expected_return_date
        THEN EXTRACT(DAY FROM CURRENT_DATE - t.expected_return_date) * 0.25
        ELSE 0
    END AS late_fee
FROM Client c
JOIN Transaction t ON c.client_id = t.client_id
JOIN Media_Item mi ON t.item_id = mi.item_id
LEFT JOIN Book b ON mi.item_id = b.item_id
LEFT JOIN Digital_Media dm ON mi.item_id = dm.item_id
LEFT JOIN Magazine mg ON mi.item_id = mg.item_id
ORDER BY c.client_id, t.date_borrowed DESC;
"""

overdue_items_report = """
SELECT
    c.client_id,
    c.name,
    t.transaction_id,
    mi.item_id,
    CASE 
        WHEN b.title IS NOT NULL THEN b.title
        WHEN dm.title IS NOT NULL THEN dm.title
        WHEN mg.title IS NOT NULL THEN mg.title
        ELSE 'Unknown'
    END AS title,
    t.date_borrowed,
    t.expected_return_date,
    EXTRACT(DAY FROM CURRENT_DATE - t.expected_return_date) * 0.25 AS late_fee
FROM Transaction t
JOIN Client c ON t.client_id = c.client_id
JOIN Media_Item mi ON t.item_id = mi.item_id
LEFT JOIN Book b ON mi.item_id = b.item_id
LEFT JOIN Digital_Media dm ON mi.item_id = dm.item_id
LEFT JOIN Magazine mg ON mi.item_id = mg.item_id
WHERE t.returned_date IS NULL AND CURRENT_DATE > t.expected_return_date;
"""

revenue_summary = """
SELECT
    c.membership_type,
    CASE 
        WHEN b.item_id IS NOT NULL THEN 'Book'
        WHEN dm.item_id IS NOT NULL THEN 'Digital Media'
        WHEN mg.item_id IS NOT NULL THEN 'Magazine'
        ELSE 'Unknown'
    END AS item_category,
    SUM(EXTRACT(DAY FROM CURRENT_DATE - t.expected_return_date) * 0.25) AS total_fees
FROM Transaction t
JOIN Client c ON t.client_id = c.client_id
JOIN Media_Item mi ON t.item_id = mi.item_id
LEFT JOIN Book b ON mi.item_id = b.item_id
LEFT JOIN Digital_Media dm ON mi.item_id = dm.item_id
LEFT JOIN Magazine mg ON mi.item_id = mg.item_id
WHERE t.returned_date IS NULL AND CURRENT_DATE > t.expected_return_date
GROUP BY c.membership_type, item_category;
"""
