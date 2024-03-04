"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, request
from models import db, connect_db, Cupcake
from seed import seed_database
from forms import CupcakeForm

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['url_pattern'] = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)

seed_database()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CupcakeForm(request.form)  # Create an instance of the form
    if request.method == 'POST' and form.validate():
        # Process form submission
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data

    return render_template('index.html', form=form)

@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    search_term = request.args.get('search_term')
    if search_term:
        cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.filter(Cupcake.flavor.ilike(f'%{search_term}%')).all()]
    else:
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

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/edit/<int:cupcake_id>', methods=['GET', 'POST'])
def edit_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if request.method == 'POST':
        # Get edit data from the form
        flavor = request.form['flavor']
        size = request.form['size']
        rating = request.form['rating']
        image = request.form['image']

        # Edit cupcake attributes
        cupcake.flavor = flavor
        cupcake.size = size
        cupcake.rating = rating
        cupcake.image = image

        db.session.commit()

        # Redirect to the home page or any other page
        return redirect('/')

    # Render the update form with the cupcake data
    return render_template('edit_cupcake.html', cupcake=cupcake)