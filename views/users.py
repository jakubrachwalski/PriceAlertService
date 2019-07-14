__author__ = 'Jakub Rachwalski'

from flask import Blueprint, render_template, request, url_for, redirect, session
# from models.alert import Alert
# from models.item import Item
from models.user import User, error
import json


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # process the data

        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return email
        except error.UserError as e:
            return e.message

        # User(email, password).save_to_mongo()

    return render_template('users/register_user.html')

@user_blueprint.route("/login", methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # process the data

        email = request.form['email']
        password = request.form['password']

        try:
            if User.login_valid(email, password):
                session['email'] = email
                return email
        except error.WrongPassword as e:
            return e.message

        # User(email, password).save_to_mongo()

    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('.login_user'))
