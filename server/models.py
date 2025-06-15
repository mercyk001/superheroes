from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from sqlalchemy.orm import validates #for the validations

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

#HERO
class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)

   # def __repr__(self):
   #     return f'<Hero {self.name}>'
   
   #relationship
    hero_powers =db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
   
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'hero_powers': [hero_power.power.to_dict() for hero_power in self.hero_powers]
        }
   
   
#POWER
class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False) 
   
   
   #relationship
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    
    #validations for description
    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
   
   
   
   
   #HEROPOWER
   
class HeroPower(db.Model):
    __tablename__= 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)
       
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)  
    
    #relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')
    
    ##validations for strength
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: Strong, Weak, Average.")
        return value
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'hero': {
                'id': self.hero.id,
                'name': self.hero.name,
                'super_name': self.hero.super_name                
            },
            'power': {
                'id': self.power.id,
                'name': self.power.name,
                'description': self.power.description
            }
        }