"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template, redirect
from models import db, connect_db, Cupcake
from seed import seed_database

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)

seed_database()

# Make routes for the following:
# GET /api/cupcakes : Get data about all cupcakes. Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}. The values should come from each cupcake instance.
# GET /api/cupcakes/[cupcake-id] : Get data about a single cupcake. Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}. This should raise a 404 if the cupcake cannot be found.
# POST /api/cupcakes : Create a cupcake with flavor, size, rating and image data from the body of the request. Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
# Test that these routes work in Insomnia.
# We’ve provided tests for these three routes; these test should pass if the routes work properly.
# You can run our tests like:
# (venv) $python -m unittest -v tests

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    data = request.json
    cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None
    )
    db.session.add(cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)