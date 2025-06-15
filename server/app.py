from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

from models import db, Hero, Power, HeroPower

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Superheroes API!"


#ROUTES
#GET ROUTES
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
            } for hero in heroes]), 200
    
    
    
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict()), 200
    return jsonify({"error": "Hero not found"}), 404



@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200



@app.route("/powers/<int:id>", methods=["GET"])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict()), 200
    return jsonify({"error": "Power not found"}), 404


#PATCH ROUTES

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)

    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    new_description = data.get("description")

    if not new_description:
        return jsonify({"errors": ["Description is required."]}), 400

    try:
        power.description = new_description 
        db.session.commit()
        return jsonify(power.to_dict()), 200

    except ValueError as ve:
        db.session.rollback()
        return jsonify({"errors": [str(ve)]}), 400

    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["Something went wrong."]}), 500

    
    
    
#POST ROUTES
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()

    try:
        new_hero_power = HeroPower(
            strength=data.get("strength"),
            power_id=data.get("power_id"),
            hero_id=data.get("hero_id")
        )
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify(new_hero_power.to_dict()), 201

    except ValueError as ve:
        return jsonify({"errors": [str(ve)]}), 400
    except Exception:
        return jsonify({"errors": ["validation errors"]}), 400   
               
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)