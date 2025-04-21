import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

# Familiar sync code
conn = psycopg.Connection.connect()
cur = conn.execute("select now()")
print(cur.fetchone()[0])