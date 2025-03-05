from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.pool
import os

app = Flask(__name__)

# PostgreSQL Connection Pool
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://renderdb_tkpw_user:kgyb4KrE32MydGYXtaUcbw7Yl38CG9nv@dpg-cv40aud2ng1s73dbua6g-a/renderdb_tkpw')
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)

@app.route('/')
def home():
    return render_template('index.html')

# Add a new place
@app.route('/add_place', methods=['POST'])
def add_place():
    data = request.json
    conn = get_db_connection()
    with conn.cursor() as cursor:
        query = "INSERT INTO places (name, description, location) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['name'], data['description'], data['location']))
        conn.commit()
    release_db_connection(conn)
    return jsonify({"message": "Place added successfully!"})

# Get all places
@app.route('/places', methods=['GET'])
def get_places():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, visit_count FROM places")
        places = cursor.fetchall()
    release_db_connection(conn)
    return jsonify([{"id": p[0], "name": p[1], "visit_count": p[2]} for p in places])

# Get top visited places
@app.route('/top_places', methods=['GET'])
def get_top_places():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT name, visit_count FROM places ORDER BY visit_count DESC LIMIT 5")
        places = cursor.fetchall()
    release_db_connection(conn)
    return jsonify([{"name": p[0], "visit_count": p[1]} for p in places])

# Increase visit count
@app.route('/increase_visit_count', methods=['POST'])
def increase_visit_count():
    data = request.json
    conn = get_db_connection()
    with conn.cursor() as cursor:
        query = "UPDATE places SET visit_count = visit_count + 1 WHERE id = %s"
        cursor.execute(query, (data['place_id'],))
        conn.commit()
    release_db_connection(conn)
    return jsonify({"message": "Visit count updated!"})

if __name__ == '__main__':
    app.run(debug=True)
