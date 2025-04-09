import os
import openpyxl
import pandas as pd
from psycopg2 import sql 
from dotenv import load_dotenv
from db_connection import PostgresDB

def main(test=False):
    """Execute the data parsing and population logic."""
    load_dotenv()

    PATH = os.getenv("EXCEL_PATH")
    SHEET_NAMES = ['Client', 'Transaction', 'MediaItem', 'Book', 'Magazine', 'DigitalMedia']

    if not PATH: 
        raise ValueError("EXCEL_PATH is not set in the environment.")
    
    tables_data = {}

    # Parse data    
    for sheet in SHEET_NAMES: 
        workbook = read_sheet(PATH, sheet)  
        tables_data[sheet] = parse_workbook(sheet, workbook)            

    # Populate DB
    for sheet in SHEET_NAMES:     
        data = tables_data[sheet]
        if not data: 
            print(f"[SKIPPED] {sheet}: empty or failed to parse. No rows inserted.")
            continue
            
        # Include test routing. Shows relation insertions
        if test: 
            target_table = "Book"
            populate_table_test(sheet, data, target_table)
        else:        
            populate_table(sheet, data) 

def read_sheet(file_path, excel_sheet_name=None): 
    """Read a specified sheet in a given excel file."""
    try:
        return pd.read_excel(file_path, sheet_name=excel_sheet_name)
    except Exception as e: 
        print(f"Failed to read sheet '{excel_sheet_name}': '{e}'")
        return pd.DataFrame() # Return empty dataframe to safely skip

def parse_workbook(table_name, workbook):
    """Parse a given workbook, store information."""
    sheet_store = []

    # Store the information as a list of dict objects
    for _, row in workbook.iterrows(): 
        # Skip completely empty rows
        if row.isnull().all():
            continue

        # Skip rows with only occupied cell
        for index, cell in enumerate(row):
            if index == 0:
                continue
            if not pd.isnull(cell):
                break
        else:
            continue # Skip row

        data = {}

        for col_name in workbook.columns:
            value = row[col_name]

            # Modify data
            if isinstance(value, float) and value.is_integer():
                value = int(value) 
            
            if isinstance(value, pd.Timestamp):
                value = value.date() # Remove time part
            
            # Store the field 
            data[col_name] = value
                
        sheet_store.append(data)
        
    return sheet_store

def populate_table_test(table_name, table_data, target_table, verbose=True): 
    if not target_table.strip(): raise ValueError("Invalid table name.")
    if print: 
        if table_name != target_table: 
            pass
        else: 
            for row in table_data: 
                print(f"[INSERTED into {table_name}] {row}\n")        

def populate_table(table_name, table_data): 
    """Populate a table in the PostgreSQL database."""
    conn, db = open_db_conn()

    if not conn: 
        print(f"[SKIPPED] {table_name}: could not connect to DB.")
        return
    
    # A cursor is a control structure that allows the execution of SQL queries in the db
    cursor = conn.cursor()

    for row in table_data: 
        insert_row(cursor, table_name, row)
        print(f"[INSERTED into {table_name}] {row}")

    # Cleanup
    conn.commit()
    cursor.close()
    db.close()

def insert_row(cursor, table_name, row_data): 
    """Insert a row into a table in the PostgreSQL database."""
    columns = list(row_data.keys())
    values =  list(row_data.values())

    # Use psycopg2.sql to safely interpolate identifiers and placeholders (prevents SQL injection)
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
            table = sql.Identifier(table_name), 
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )

    try: 
        cursor.execute(query, values)
    except Exception as e: 
        print(f"[ERROR] Failed to insert into {table_name}: {e}.")

def open_db_conn(): 
    """Establish a connection to the PostgreSQL database."""
    try: 
        db = PostgresDB(password=os.getenv("DB_PASSWORD"))
        conn = db.connect()
        return conn, db
    except Exception as e:
        print(f"[ERROR] Failed to open DB connection: {e}")
        return None, None

if __name__ == "__main__":
    main(True)