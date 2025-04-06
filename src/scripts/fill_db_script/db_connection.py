import psycopg2

class PostgresDB:
    def __init__(self,
                 host="libdb-25co-postgres.cajikaswgj3d.us-east-1.rds.amazonaws.com",
                 dbname="postgres",
                 user="LibDB_25Co",
                 password="null"):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.dbname,
                user=self.user,
                password=self.password
            )
            print("DB connection successful")
            return self.conn
        except Exception as e:       
            print(f"[ERROR] DB connection failure: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            print("DB connection closed")

# Only run when called directly
if __name__ == "__main__":
    db = PostgresDB()
    conn = db.connect()
