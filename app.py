from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.pool
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://renderdb_tkpw_user:kgyb4KrE32MydGYXtaUcbw7Yl38CG9nv@dpg-cv40aud2ng1s73dbua6g-a/renderdb_tkpw')
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)

@app.route('/')
def home():
    return render_template('index.html')

# Add a new place (added by locals)
@app.route('/add_place', methods=['POST'])
def add_place():
    data = request.json
    conn = get_db_connection()
    with conn.cursor() as cursor:
        query = "INSERT INTO places (name, description, district, visit_count) VALUES (%s, %s, %s, 0)"
        cursor.execute(query, (data['name'], data['description'], data['district']))
        conn.commit()
    release_db_connection(conn)
    return jsonify({"message": "Place added successfully!"})

# Get places by district (show hidden places)
@app.route('/places', methods=['GET'])
def get_places():
    district = request.args.get('district')
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, description, visit_count FROM places WHERE district = %s ORDER BY visit_count ASC LIMIT 5", (district,))
        places = cursor.fetchall()
    release_db_connection(conn)
    return jsonify([{"id": p[0], "name": p[1], "description": p[2], "visit_count": p[3]} for p in places])

if __name__ == '__main__':
    app.run(debug=True)

