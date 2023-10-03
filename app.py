"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hushyourmouth"

connect_db(app)


@app.route('/')
def root():
    """Shows homepage."""

    return render_template('index.html')



@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON with all cupcakes."""

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)



@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Returns data on a specific cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())



@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a cupcake, and returns data about the new cupcake."""

    cupcake = Cupcake(
        flavor = request.json['flavor'],
        rating = request.json['rating'],
        size = request.json['size'],
        image = request.json['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)



@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates data in a specific cupcake, and returns the new data."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())



@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes specific cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

