from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret secret'

connect_db(app)

@app.route('/')
def home():
    """home page"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """Shows all cupcakes in system

       Returns JSON like:
        {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Adds a cupcake, returns data about new cupcake

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    # You want a Post request to return HTTP status of 201 b/c 201 means it was posted correctly
    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Updates a cupcakes info - id, flavor, rating, size, or image
        Will return info in JSON like python dictionary
    """
    data = request.json
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Deletes a cupcake and returns a delete success message"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted!")