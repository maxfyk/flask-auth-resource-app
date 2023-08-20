import os
import json

DB_PATH = 'db.json'

if not os.path.isfile(DB_PATH):
    DB_PATH = '../db.json'


def load_db():
    with open(DB_PATH, 'r') as f:
        return json.load(f)


def save_db_changes(db):
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=4)
