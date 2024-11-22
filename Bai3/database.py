import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="sach",
        user="postgres",
        password="1234567890",
        cursor_factory=DictCursor
    )
