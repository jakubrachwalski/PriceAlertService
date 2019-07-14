__author__ = 'Jakub Rachwalski'

from flask import Blueprint, render_template, request, url_for, redirect, session
from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user import requires_login


alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route("/")
@requires_login
def index():
    # alerts = Alert.all()
    print(session['email'])
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route("/new", methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        # process the data
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        item_name = request.form['item_name']
        user_email = session['email']

        store = Store.get_by_url(item_url)
        # print(store)
        item = Item(item_url, store.tag_name, store.query)
        # print(item)
        item.load_price()
        # print(item.load_price())
        item.save_to_mongo()

        Alert(item_name, item._id, price_limit, user_email).save_to_mongo()

        return redirect(url_for('.index'))

    else:

        return render_template('alerts/new_alert.html')


@alert_blueprint.route("/edit/<string:alert_id>", methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):

    alert = Alert.get_by_id(alert_id)

    if request.method == 'POST':
        if alert.user_email == session['email']:
            alert.price_limit = float(request.form['price_limit'])
            alert.save_to_mongo()

            return redirect(url_for('.index'))

    else:
        return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route("/delete/<string:alert_id>")
@requires_login
def remove_alert(alert_id):

    alert = Alert.get_by_id(alert_id)

    if alert.user_email == session['email']:
        item = Item.get_by_id(alert.item_id)
        item.remove_from_mongo()
        alert.remove_from_mongo()

    return redirect(url_for('.index'))
