import os
import sqlite3

# Step 1: Delete existing database files if they exist
if os.path.exists('predictions.db'):
    os.remove('predictions.db')
    print("🗑️ Deleted predictions.db")

if os.path.exists('admin.db'):
    os.remove('admin.db')
    print("🗑️ Deleted admin.db")

# Step 2: Recreate predictions.db with required table
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
print("✅ predictions.db initialized")

# Step 3: Recreate admin.db with empty admin table (no default admin)
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
