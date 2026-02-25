import os
import sys

# Get the project root directory
current_file = os.path.abspath(__file__)
database_dir = os.path.dirname(current_file)
backend_dir = os.path.dirname(database_dir)
project_root = os.path.dirname(backend_dir)

# Add project root to sys.path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from backend.database.database import Base, engine

def init_db():
    """Initializes the SQLite database (creates tables)."""
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized successfully!")

if __name__ == "__main__":
    init_db()
