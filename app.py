"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
import validators

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/')
def show_homepage():
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_all_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    # request.json actually evaluates to a dictionary in Python, so we can use the same trick as in the last exercise
    # (pet adoption website) and just spread (or splat) the request.json dictionary into our Cupcake SQLAlchemy object,
    # instead of having to enter each field one at a time manually
    
    json = request.json

    if not json['image'] or not validators.url(json['image']):
        json['image'] = None

    new_cupcake = Cupcake(**json)
    db.session.add(new_cupcake)
    db.session.commit()

    json_resp = jsonify(cupcake=new_cupcake.serialize())

    return (json_resp, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def edit_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    flavor = request.json.get("flavor", cupcake.flavor)
    size = request.json.get("size", cupcake.size)
    rating = request.json.get("rating", cupcake.rating)
    image = request.json.get("image", cupcake.image)

    if flavor:
        cupcake.flavor = flavor

    if size:
        cupcake.size = size

    if rating:
        cupcake.rating = rating

    if image:
        cupcake.image = image

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")