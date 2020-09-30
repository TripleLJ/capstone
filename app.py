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
from forms import *
from wtforms import TextField, BooleanField
from wtforms.validators import Required
# from auth import AuthError, requires_auth, verify_decode_jwt
from auth import get_token_auth_header, verify_decode_jwt, check_permissions

from functools import wraps
from jose import jwt
from urllib.request import urlopen


def requires_auth2(permission=''):
    def requires_auth2decor(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            payload = verify_decode_jwt(jwt)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth2decor










































def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

 # Teams
 # ------------------------------------------------
  @app.route('/headers')
  @requires_auth2('create:teams')
  def headers(jwt):
      jwt = get_token_auth_header()
      return jwt



  @app.route('/')
  def index():
      return redirect(url_for('get_teams'))

  @app.route('/teams')
  @requires_auth2('create:teams')
  def get_teams(jwt):
      teams = Team.query.all()
      return render_template('pages/teams.html', teams=teams)

  @app.route('/login')
  def login():

      return render_template('pages/login.html')

  @app.route('/logout')
  def logout():

      return render_template('pages/logout.html')

  @app.route('/teams/<team_id>')
  def get_team(team_id):
      team = Team.query.get(team_id)
      players = Player.query.filter_by(team_id=team_id)
      return render_template('pages/team.html', team=team, players=players)

  @app.route('/teams/<team_id>/edit')
  def edit_team(team_id):
      team = Team.query.get(team_id)
      players = Player.query.filter_by(team_id=team_id)
      form = TeamForm(secret_key=os.urandom(32))
      return render_template('forms/edit_team.html', team=team, players=players, form=form)


  @app.route('/teams/create')
  def create_team_form():
      form = TeamForm(secret_key=os.urandom(32))
      return render_template('forms/new_team.html', form=form)



  @app.route('/teams/<team_id>/delete', methods=['DELETE', 'GET'])
  def deleting_team(team_id):
      error = False
      try:
          team = Team.query.get(team_id)
          players = Player.query.filter_by(team_id=team_id)
          db.session.delete(team)
          for player in players:
              db.session.delete(player)
          db.session.commit()
      except():
          db.session.rollback()
          error = True
      finally:
          db.session.close()
      if error:
          flash('An error occured. Could not be deleted')
          abort(500)
      else:
          flash('Team ' + team.name + ' was deleted.')
          return redirect(url_for('get_teams'))


  @app.route('/teams/create', methods=['POST'])
  def create_team_submission():
      error = False
      body = {}
      try:
          name =request.form.get('name')
          city = request.form.get('city')
          image = request.form.get('image')
          color1 = request.form.get('color1')
          color2 = request.form.get('color2')

          team = Team(name=name, city=city, image=image, color1=color1, color2=color2)

          db.session.add(team)
          db.session.commit()

          body['id'] = team.id
          body['name'] = team.name
          body['city'] = team.city
          body['image'] = team.image
          body['color1'] = team.color1
          body['color2'] = team.color2

      except():
          db.session.rollback()
          error = True
          print(sys.exc_info())
      finally:
          db.session.close()
          if error:
              flash('An error occured. Team ' + request.form['name'] + ' could not be created!')
              abort(500)
          else:
            flash('Team ' + request.form['name'] + ' was successfully created!')
            return redirect(url_for('get_teams'))

  @app.route('/teams/<team_id>/edit', methods=['PATCH','POST'])
  def edit_team_submission(team_id):
      error = False
      body = {}
      try:
          team = Team.query.get(team_id)

          team.name =request.form.get('name')
          team.city = request.form.get('city')
          team.image = request.form.get('image')
          team.color1 = request.form.get('color1')
          team.color2 = request.form.get('color2')



          db.session.commit()

          body['id'] = team.id
          body['name'] = team.name
          body['city'] = team.city
          body['image'] = team.image
          body['color1'] = team.color1
          body['color2'] = team.color2

      except():
          db.session.rollback()
          error = True
          print(sys.exc_info())
      finally:
          db.session.close()
          if error:
              flash('An error occured. Team ' + request.form['name'] + ' could not be updated!')
              abort(500)
          else:
            flash('Team ' + request.form['name'] + ' was successfully updated!')
            return redirect(url_for('get_teams'))


# Players
# ------------------------------------------------


  @app.route('/players')
  def get_players():
      players = Player.query.all()
      return render_template('pages/players.html', players=players)


  @app.route('/players/<player_id>')
  def get_player(player_id):
      player = Player.query.get(player_id)
      team = Team.query.get(player.team_id)
      return render_template('pages/player.html', player=player, team=team)

  @app.route('/players/<player_id>/edit')
  def edit_player(player_id):
      player = Player.query.get(player_id)
      team = Team.query.get(player.team_id)
      form = PlayerForm(secret_key=os.urandom(32))
      return render_template('forms/edit_player.html', player=player, team=team, form=form)



  @app.route('/players/<player_id>/delete', methods=['DELETE', 'GET'])
  def deleting_player(player_id):
      error = False
      try:
          player = Player.query.get(player_id)
          db.session.delete(player)
          db.session.commit()
      except():
          db.session.rollback()
          error = True
      finally:
          db.session.close()
      if error:
          flash('An error occured. Could not be deleted')
          abort(500)
      else:
          flash('Player ' + player.last_name + ' was deleted.')
          return redirect(url_for('get_players'))

  @app.route('/players/create')
  def create_player():
      form = PlayerForm(secret_key=os.urandom(32))
      return render_template('forms/new_player.html', form=form)

  @app.route('/players/create', methods=['PATCH','POST'])
  def create_player_submission():
      error = False
      body = {}
      try:
          first_name =request.form.get('first_name')
          last_name = request.form.get('last_name')
          image = request.form.get('image')
          team_id = request.form.get('team_id')
          number = request.form.get('number')
          position = request.form.get('position')

          player = Player(first_name=first_name, last_name=last_name, image=image, number=number, team_id=team_id, position=position)




          db.session.add(player)
          db.session.commit()

          body['id'] = player.id
          body['first_name'] = player.first_name
          body['last_name'] = player.last_name
          body['image'] = player.image
          body['number'] = player.number
          body['team_id'] = player.team_id

      except():
          db.session.rollback()
          error = True
          print(sys.exc_info())
      finally:
          db.session.close()
      if error:
          flash('An error occured. Player ' + request.form['last_name'] + ' could not be created!')
          abort(500)
      else:

          flash('Player ' + request.form['last_name'] + ' was successfully created!')

          return redirect(url_for('get_players'))

  @app.route('/players/<player_id>/edit', methods=['PATCH','POST'])
  def edit_player_submission(player_id):
      error = False
      body = {}
      try:
          player = Player.query.get(player_id)

          player.first_name =request.form.get('first_name')
          player.last_name = request.form.get('last_name')
          player.image = request.form.get('image')
          player.team_id = request.form.get('team_id')
          player.number = request.form.get('number')
          player.position = request.form.get('position')




          db.session.commit()

          body['id'] = player.id
          body['first_name'] = player.first_name
          body['last_name'] = player.last_name
          body['image'] = player.image
          body['number'] = player.number
          body['team_id'] = player.team_id

      except():
          db.session.rollback()
          error = True
          print(sys.exc_info())
      finally:
          db.session.close()
      if error:
          flash('An error occured. Player ' + request.form['last_name'] + ' could not be updated!')
          abort(500)
      else:

          flash('Player ' + request.form['last_name'] + ' was successfully updated!')

          return redirect(url_for('get_players'))



  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
