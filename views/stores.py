__author__ = 'Jakub Rachwalski'

from flask import Blueprint, render_template, request, url_for, redirect
# from models.alert import Alert
# from models.item import Item
from models.user import requires_admin, requires_login
from models.store import Store
import json


store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route("/")
@requires_login
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@store_blueprint.route("/new", methods=['GET', 'POST'])
@requires_admin
def new_store():
    if request.method == 'POST':
        # process the data

        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = request.form['query']
        query = query.replace("\'", "\"")
        query = json.loads(query)

        Store(name, url_prefix, tag_name, query).save_to_mongo()
        return redirect(url_for('.index'))

    else:

        return render_template('stores/new_store.html')


@store_blueprint.route("/edit/<string:store_id>", methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):

    store = Store.get_by_id(store_id)

    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        query = request.form['query']
        query = query.replace("\'", "\"")
        store.query = json.loads(query)

        store.save_to_mongo()
        return redirect(url_for('.index'))

    else:
        return render_template('stores/edit_store.html', store=store)


@store_blueprint.route("/delete/<string:store_id>")
@requires_admin
def remove_store(store_id):

    store = Store.get_by_id(store_id)
    store.remove_from_mongo()

    return redirect(url_for('.index'))
