"""
Authors: Holden Vail, Michael Stang, Logan Smith, Blake Carlson, Nifemi Lawal
Class: EECS 447
Assignment: Database Design Project Part 5: Physical Database Design
"""

import psycopg2

# Database connection parameters
DB_HOST = "libdb-25co-postgres.cajikaswgj3d.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "LibDB_25Co"
DB_PASSWORD = "null"        # Replace this with the master password

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
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


def main():
    """CLI for interacting with DB"""
    pass

main()