"""Home related views."""
from datetime import datetime
from flask import request, render_template, flash, Blueprint
import json
from moontracker.assets import supported_assets
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
                           app_markets_json=json.dumps(supported_assets))


@home_blueprint.route('/appMarkets.js', methods=['GET'])
def app_markets():
    """Generate JavaScript for appMarkets."""
    return 'appMarkets = ' + json.dumps(supported_assets)