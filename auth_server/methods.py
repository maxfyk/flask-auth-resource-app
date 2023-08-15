import json


def load_db():
    with open('db.json', 'r') as f:
        return json.load(f)


def save_db(db):
    with open('db.json', 'w') as f:
        json.dump(db, f, indent=4)
