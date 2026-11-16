
from database.db import init_db, DB_PATH

init_db()

print("Database initialized successfully!")
print(f"Database location: {DB_PATH}")
