"""Home related views."""
import os
from flask import request, render_template, flash, Blueprint, current_app
from flask import send_from_directory
import json
from moontracker.assets import supported_assets
from moontracker.times import supported_durations
from moontracker.views.alert_utils import AlertForm, make_new_alert

home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Code for the homepage."""
    form = AlertForm(request.form)
    if request.method == 'POST' and form.validate():
        make_new_alert(form)
        flash("Alert is set!")
    return render_template('index.html', form=form,
                           app_markets_json=json.dumps(supported_assets),
                           app_durations_json=json.dumps(supported_durations))


@home_blueprint.route('/appMarkets.js', methods=['GET'])
def app_markets():
    """Generate JavaScript for appMarkets."""
    return 'appMarkets = ' + json.dumps(supported_assets)


@home_blueprint.route('/appDurations.js', methods=['GET'])
def app_durations():
    """Generate JavaScript for appDurations."""
    return 'appDurations = ' + json.dumps(supported_durations)


@home_blueprint.route('/favicon.ico')
def favicon():
    """Get the favicon."""
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
