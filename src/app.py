"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Vehicle, People, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# [GET] /people Listar todos los registros de people en la base de datos.
@app.route('/people', methods=['GET'])
def get_people_all():
    try:
        people_list = []
        people = db.session.execute(db.select(People)).scalars().all()
        for ppl in people:
            people_list.append(ppl.serialize())
        return jsonify({"result": people_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# [GET] /planets Listar todos los registros de planets en la base de datos.
@app.route('/planets', methods=['GET'])
def get_planets_all():
    try:
        Lista_response = []
        Lista_Planetas = db.session.execute(db.select(Planet)).scalars().all()
        for item in Lista_Planetas:
            Lista_response.append(item.serialize())
        return jsonify({"result": Lista_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# [GET] /users Listar todos los usuarios del blog.
@app.route('/users', methods=['GET'])
def get_users_all():
    try:
        Lista_response = []
        result_list = db.session.execute(db.select(User)).scalars().all()
        for item in result_list:
            Lista_response.append(item.serialize())
        return jsonify({"result": Lista_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# [GET] /people/<int:people_id> Muestra la información de un solo personaje según su id.
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    people = db.session.execute(db.select(People).filter_by(
        id=people_id)).scalar_one_or_none()

    if people is not None:
        return jsonify(people.serialize())
    else:
        return jsonify({'response': f"No se encontro el personaje con el id {people_id}"}), 404

# [GET] /planets/<int:planet_id> Muestra la información de un solo planeta según su id.
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets_by_id(planet_id):
   try:
        Lista_response = []
        result_list = db.session.execute(db.select(User)).scalars().all()
        for item in result_list:
            Lista_response.append(item.serialize())
        return jsonify({"result": Lista_response})
   except Exception as e:
        return jsonify({"error": str(e)}), 500


#[GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_favorites_by_user(user_id):
      try:
        Lista_response = []
        result_list = db.session.execute(db.select(Favorite).filter_by(user_id=user_id)).scalars().all()
        for item in result_list:
            Lista_response.append(item.serialize())
        return jsonify({"result": Lista_response})
      except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#[POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
@app.route('/favorite/planet/<int:planet_id>/<int:usuario_id>', methods=['POST'])
def add_favorites_planet_by_id_to_User(planet_id, usuario_id):
        
        # Verificar si planeta existe
        planet = db.session.get(Planet, planet_id)
        if planet is None:
            return jsonify({'error': f"No se encontró el planeta con el id {planet_id}"}), 404

        # Verificar si ya es favorito
        existing_fav = db.session.execute(
            db.select(Favorite).filter_by(user_id=usuario_id, planet_id=planet_id)
        ).scalar_one_or_none()

        if existing_fav:
            return jsonify({'message': 'Este planeta ya está en tus favoritos'}), 200

        # Crear favorito
        new_favorite = Favorite(user_id=usuario_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({'message': f'Planeta con id {planet_id} añadido a favoritos'}), 201

#[POST] /favorite/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
@app.route('/favorite/people/<int:people_id>/<int:usuario_id>', methods=['POST'])
def add_favorites_people_by_id_to_User(people_id, usuario_id):
        
        # Verificar si planeta existe
        people = db.session.get(People, people_id)
        if people is None:
            return jsonify({'error': f"No se encontró el planeta con el id {people_id}"}), 404

        # Verificar si ya es favorito
        existing_fav = db.session.execute(
            db.select(Favorite).filter_by(user_id=usuario_id, people_id=people_id)
        ).scalar_one_or_none()

        if existing_fav:
            return jsonify({'message': 'Este Personaje ya está en tus favoritos'}), 200

        # Crear favorito
        new_favorite = Favorite(user_id=usuario_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({'message': f'People con id {people_id} añadido a favoritos'}), 201

#[DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
@app.route('/favorite/planet/<int:planet_id>/<int:usuario_id>', methods=['DELETE'])
def delete_favorites_planet_by_id_to_User(planet_id, usuario_id):
    try:
        favorite = db.session.execute(
            db.select(Favorite).filter_by(user_id=usuario_id, planet_id=planet_id)
        ).scalar_one_or_none()

        if favorite is None:
            return jsonify({'error': f'No se encontró un favorito con planet_id {planet_id} para este usuario'}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'message': f'Favorito con planet_id {planet_id} eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#[DELETE] /favorite/people/<int:people_id> Elimina un people favorito con el id = people_id.
@app.route('/favorite/people/<int:people_id>/<int:usuario_id>', methods=['DELETE'])
def delete_favorites_people_by_id_to_User(people_id, usuario_id):
    try:
        favorite = db.session.execute(
            db.select(Favorite).filter_by(user_id=usuario_id, people_id=people_id)
        ).scalar_one_or_none()

        if favorite is None:
            return jsonify({'error': f'No se encontró un favorito con people_id {people_id} para este usuario'}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'message': f'Favorito con people_id {people_id} eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500









# Seleccionar todos db.session.execute(db.select(Modelo)).scalars().all() - Devuelve todo lo encontrado en el modelo a consultar.
# Filtrar por - db.select(Modelo).filter_by(nombre_atributo=valor)
# Para agregar datos a la bd.
# people = People(name=valor_name, birth_year=valor_birth_year, eye_color=valor_eye_color)
# db.session.add(people)
# db.session.commit()

# One or none = scalar_one_or_none() - Devuelve un valor encontrado o None
# One = scalar_one() - Devolver un resultado exacto, devuelve un error, si lo que encontró es mas o menos.
# One or 404 = db.get_or_404(Model, 1) - Lanza un 404 sino encuentra nada.

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/people/<name>', methods=['GET'])
def handle_people_by_name(name):
    people = db.session.execute(
        db.select(People).filter_by(name=name)).scalar_one_or_none()
    if not None:
        return jsonify(people.serialize())


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
