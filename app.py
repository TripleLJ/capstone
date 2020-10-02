import os
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Team, Player, db
import json
import logging
import sys
from logging import Formatter, FileHandler
from flask_wtf import Form

from wtforms import TextField, BooleanField
from wtforms.validators import Required
from auth import get_token_auth_header, verify_decode_jwt, check_permissions, AuthError, requires_auth

from functools import wraps
from jose import jwt
from urllib.request import urlopen






def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

 # Teams
 # ------------------------------------------------
  @app.route('/headers')
  @requires_auth('create:teams')
  def headers(jwt):
      jwt = get_token_auth_header()
      return jwt

  @app.route('/login')
  def login():
      return 'Login'

  @app.route('/logout')
  def logout():
      return 'Logout'

  @app.route('/login-results')
  def loginresults():

      return 'Login Results'





  @app.route('/teams')
  def get_teams():
      teams = Team.query.all()
      teamsarray = []
      for team in teams:
          teamsarray.append(team.format())
      return jsonify ({
          'success': True,
          'teams': teamsarray
          })


  @app.route('/teams/<team_id>')
  def get_team(team_id):
      team = Team.query.get(team_id)
      teamsarray = []
      teamsarray.append(team.format())
      return jsonify ({
        'success': True,
        'team': teamsarray
        })



  @app.route('/teams/<team_id>', methods=['DELETE'])
  @requires_auth('delete:teams')
  def deleting_team(jwt, team_id):
      error = False
      try:
          team = Team.query.get(team_id)
          players = Player.query.filter_by(team_id=team_id)
          team.delete()
          for player in players:
              player.delete()

      except():
          error = True

      if error:
          abort(500)
      else:
          return jsonify ({
            'success': True,
            'deleted_team_id': team_id
            })


  @app.route('/teams', methods=['POST'])
  @requires_auth('create:teams')
  def create_team_submission(jwt):
      error = False
      body = {}
      try:
          body = request.get_json()
          name = body['name']
          city = body['city']
          image = body['image']
          color1 = body['color1']
          color2 = body['color2']

          team = Team(name=name, city=city, image=image, color1=color1, color2=color2)
          team.insert()

      except():
          error = True

      if error:
          abort(500)
      else:
          teamsarray = []
          teamsarray.append(team.format())
          return jsonify ({
          'success': True,
          'created_team': teamsarray
          })

  @app.route('/teams/<team_id>', methods=['PATCH'])
  @requires_auth('edit:teams')
  def edit_team_submission(jwt, team_id):
      error = False
      body = {}
      try:
          team = Team.query.get(team_id)

          body['id'] = team.id
          body['name'] = team.name
          body['city'] = team.city
          body['image'] = team.image
          body['color1'] = team.color1
          body['color2'] = team.color2

          team.update()



      except():

          error = True

      finally:
          if error:
              abort(500)
          else:
            teamsarray = []
            teamsarray.append(team.format())
            return jsonify ({
            'success': True,
            'team': teamsarray
            })


# Players
# ------------------------------------------------


  @app.route('/players')
  def get_players():
      players = Player.query.all()
      playersarray = []
      for player in players:
          playersarray.append(player.format())
      return jsonify ({
        'success': True,
        'players': playersarray
      })


  @app.route('/players/<player_id>')
  def get_player(player_id):
      player = Player.query.get(player_id)
      playersarray = []
      playersarray.append(player.format())
      return jsonify ({
        'success': True,
        'players': playersarray
      })


  @app.route('/players/<player_id>', methods=['DELETE'])
  @requires_auth('delete:players')
  def deleting_player(jwt, player_id):
      error = False
      try:
          player = Player.query.get(player_id)
          player.delete()
      except():
          error = True
      if error:
          abort(500)
      else:

          return jsonify ({
            'success': True,
            'deleted_player': player_id
            })


  @app.route('/players', methods=['POST'])
  @requires_auth('create:players')
  def create_player_submission(jwt):
      error = False
      body = {}
      try:
          body = request.get_json()
          first_name = body['first_name']
          last_name = body['last_name']
          image = body['image']
          team_id = body['team_id']
          number = body['number']
          position = body['position']

          player = Player(first_name=first_name, last_name=last_name, image=image, number=number, team_id=team_id, position=position)
          player.insert()

      except():
          error = True
      if error:
          abort(500)
      else:
          playersarray = []
          playersarray.append(player.format())
          return jsonify ({
            'success': True,
            'created_player': playersarray
            })



  @app.route('/players/<player_id>', methods=['PATCH'])
  @requires_auth('edit:players')
  def edit_player_submission(jwt, player_id):
      error = False
      body = {}

      try:
          player = Player.query.get(player_id)


          body = request.get_json()

          player.first_name = body['first_name']
          player.last_name = body['last_name']
          player.image = body['image']
          player.team_id = body['team_id']
          player.number = body['number']
          player.position = body['position']



          player.update()


      except():
          error = True

      if error:
          abort(500)
      else:
          player = Player.query.get(player_id)
          playersarray = []
          playersarray.append(player.format())
          return jsonify ({
            'success': True,
            'player': playersarray
            })



  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Could not be found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Could not be processed"
        }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(500)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server"
    }), 500

  @app.errorhandler(401)
  def not_authorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Not authorized"
    }), 401
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
