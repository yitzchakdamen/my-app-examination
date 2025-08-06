from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', 'password'),
        database=os.getenv('DB_NAME', 'testdb')
    )

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        with open("init_db.sql", "r") as f:
            sql_script = f.read()
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        conn.commit()
    except Exception as e:
        print("Error initializing database:", e)
    finally:
        cursor.close()
        conn.close()

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (%s)", (data['name'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'}), 201


initialize_database()
app.run(host='0.0.0.0', port=8080)
