import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Define the database URL as a variable
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://renderdb_tkpw_user:kgyb4KrE32MydGYXtaUcbw7Yl38CG9nv@dpg-cv40aud2ng1s73dbua6g-a/renderdb_tkpw')

# ✅ Configure SQLAlchemy with the database URL
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Define the Places model
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    district = db.Column(db.String(100), nullable=False)
    visit_count = db.Column(db.Integer, default=0)

# ✅ Create the database tables (run this once)
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Welcome to the Travel Itinerary API!"
    

# ✅ Route for adding a new place
@app.route('/add_place', methods=['POST'])
def add_place():
    data = request.json
    new_place = Place(
        name=data['name'],
        description=data.get('description', ''),
        district=data['district'],
        visit_count=0
    )
    db.session.add(new_place)
    db.session.commit()
    return jsonify({"message": "Place added successfully"}), 201

# ✅ Route for fetching places by district (sorted by visit count)
@app.route('/places/<district>', methods=['GET'])
def get_places(district):
    places = Place.query.filter_by(district=district).order_by(Place.visit_count.desc()).all()
    return jsonify([{ "id": p.id, "name": p.name, "description": p.description, "visit_count": p.visit_count} for p in places])

# ✅ Route for increasing visit count of a place
@app.route('/visit/<int:place_id>', methods=['POST'])
def increase_visit(place_id):
    place = Place.query.get(place_id)
    if place:
        place.visit_count += 1
        db.session.commit()
        return jsonify({"message": "Visit count updated"}), 200
    return jsonify({"error": "Place not found"}), 404

# ✅ Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
