"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/contact', methods=['GET'])
def get_persona():
    all_people = Contact.query.all()
    all_people_serialized = list(map(lambda x: x.serialize(), all_people))


    return jsonify(all_people_serialized), 200

@app.route('/contact', methods=['POST'])
def post_persona():

    body = request.get_json()

    # if 'full_name' not in body:
    #     raise APIException('Hermamanazo te equivocaste en el full_name', status_code=400)

    # if body["email"].find('@') == -1:
    #     raise APIException('Mamita te falta un arroba en el email', status_code=400)

    user1 = Contact(full_name=body["full_name"], email=body["email"], phone=body["phone"], address=body["address"], agenda_slug=body["agenda_slug"])
    db.session.add(user1)
    db.session.commit()

    return jsonify(user1.serialize()), 200

@app.route('/contact/<int:id>', methods=['PUT'])
def put_persona(id):

    body = request.get_json()
    user1 = Contact.query.get(id)
    if user1 is None:
        raise APIException('User not found', status_code=404)

    if "full_name" in body:
        user1.full_name = body["full_name"]
    if "email" in body:
        user1.email = body["email"]
    if "phone" in body:
        user1.phone = body["phone"]
    if "address" in body:
        user1.address = body["address"]
    if "agenda_slug" in body:
        user1.agenda_slug = body["agenda_slug"]
    db.session.commit()

    return jsonify(user1.serialize()), 200

@app.route('/contact/<int:id>', methods=['DELETE'])
def delete_persona(id):

    user1 = Contact.query.get(id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()

    return jsonify(user1.serialize()), 200


# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
