import sqlite3

conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    result TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    duration REAL
)
''')

conn.commit()
conn.close()
print("predictions.db initialized with duration column.")

import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('admin.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
conn.commit()
conn.close()
print("✅ admin.db initialized (no default admin)")