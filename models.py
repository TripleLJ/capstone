import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

# database_path = os.environ['DATABASE_URL ']
database_path = 'postgres://wrxuxsduxrrhab:1a07505a7a2afe4206e92491c773ba188be7d4380a30a2fe19958156026702ad@ec2-23-20-168-40.compute-1.amazonaws.com:5432/d1sqi37ueiaasu'

app = Flask(__name__)

db = SQLAlchemy(app)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    app.secret_key = os.urandom(32)
    app.SECRET_KEY = os.urandom(32)
    db.init_app(app)
    db.create_all()


'''
Team
'''
class Team(db.Model):
  __tablename__ = 'Team'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String)
  image = db.Column(db.String)
  color1 = db.Column(db.String)
  color2 = db.Column(db.String)
  players = db.relationship("Player", backref="team")



  def __init__(self, name, city, image, color1, color2):
    self.name = name
    self.city = city
    self.image = image
    self.color1 = color1
    self.color2 = color2


  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'city': self.city,
      'image': self.image,
      'color1': self.color1,
      'color2': self.color2,
      }
  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()



class Player(db.Model):
  __tablename__ = 'Player'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  # team_id = Column(Integer, ForeignKey('Team.id'))
  team_id = db.Column(db.Integer, db.ForeignKey('Team.id'))
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  number = db.Column(db.String)
  position = db.Column(db.String)
  image = db.Column(db.String)
  # Number is a string to avoid issues with formatting #00, #0, #06, etc.


  def __init__(self, team_id, first_name, last_name, number, image, position):
    self.team_id = team_id
    self.first_name = first_name
    self.last_name = last_name
    self.number = number
    self.image = image
    self.position = position



  def format(self):
    return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'image': self.image,
      'team_id': self.team_id
      }

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()
