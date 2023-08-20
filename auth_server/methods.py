import json

DB_FILE_PATH = 'db.json'


def load_db():
    """Load database from a json file"""
    with open(DB_FILE_PATH, 'r') as f:
        return json.load(f)


def save_db_changes(db):
    """Save changes to the database json file"""
    with open(DB_FILE_PATH, 'w') as f:
        json.dump(db, f, indent=4)
