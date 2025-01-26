import sqlite3
import csv
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Path to your SQLite database
db_path = 'database.db'

# Path to your CSV file
csv_path = 'words.csv'
recipes_path = 'recipes.csv'

# Function to import data from CSV into the database
def import_csv_to_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the words table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS words (
        id INTEGER NOT NULL,
        georgian TEXT NOT NULL,
        english TEXT NOT NULL,
        ipa TEXT,
        category TEXT,
        added_date DATE DEFAULT CURRENT_DATE,
        difficulty_level INTEGER DEFAULT 1,
        times_reviewed INTEGER DEFAULT 0,
        last_reviewed DATE
    )''')

    # Check if data is already present in the words table
    cursor.execute("SELECT COUNT(*) FROM words")
    if cursor.fetchone()[0] > 0:
        print("word already imported.")
        conn.close()
        return

    # Open and read the CSV file
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        # Skip the header row
        next(csv_reader)

        # Insert data from CSV into the database
        for row in csv_reader:
            id = row[0]
            georgian_word = row[1]
            english_translation = row[2]
            ipa = row[3] if len(row) > 3 else None
            category = row[4] if len(row) > 4 else None
            difficulty_level = int(row[5]) if len(row) > 5 else 1

            # Insert the data into the words table
            cursor.execute('''
                INSERT INTO words (id, georgian, english, ipa, category, difficulty_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id, georgian_word, english_translation, ipa, category, difficulty_level))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Words imported successfully!")




def import_recipes_to_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the words table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT,
        category VARCHAR(100),
        preparation_time VARCHAR(50),
        cooking_time VARCHAR(50)
    )''')

    # Check if data is already present in the words table
    cursor.execute("SELECT COUNT(*) FROM recipes")
    if cursor.fetchone()[0] > 0:
        print("recipe already imported.")
        conn.close()
        return

    # Open and read the CSV file
    with open(recipes_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        # Skip the header row
        next(csv_reader)

        # Insert data from CSV into the database
        for row in csv_reader:
            id = int(row[0])
            name = row[1]
            ingredients = row[2]
            instructions = row[3]
            category = row[4]
            preparation_time = row[5]
            cooking_time = row[6]

            # Insert the data into the words table
            cursor.execute('''
                INSERT INTO recipes (id, name, ingredients, instructions, category, preparation_time, cooking_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (id, name, ingredients, instructions, category, preparation_time, cooking_time))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Recipe imported successfully!")
