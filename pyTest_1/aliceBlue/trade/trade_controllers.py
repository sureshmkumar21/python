
from flask import Flask, Blueprint, flash, render_template, redirect, request, session, url_for
from flask_login import login_required
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
from aliceBlue.trade.trade_forms import TradeForm

trade_blueprint = Blueprint('trade_home', __name__, template_folder='templates', static_folder='static')

application = Flask(__name__)
application.config.from_object('config.DevelopementConfig')

history_list = []
order_list = []

@trade_blueprint.route('/trade', methods=["GET", "POST"])
@login_required
def trade():
    tradeForm = TradeForm(request.form)
    aliceBlue = OAuth2Session(application.config['CLIENT_ID'], token=session['oauth_token'])
    
    try:
        getData = aliceBlue.get('https://ant.aliceblueonline.com/api/v2/profile').json()
    except (TokenExpiredError) as e:
        print("Token expired. Login again")
        return redirect(url_for("aliceBlue_home.login"))
        
    if request.method == 'POST':
        form_data = request.form.to_dict()
        global history_list
        if tradeForm.validate():
            if request.form['submitBtn'] == 'Add':
                add_data(form_data)
            if request.form['submitBtn'] == 'SingleOrder':
                submit_order(form_data)
            if request.form['submitBtn'] == 'BulkOrder':
                submit_orders(form_data)
        else:
            flash(u'One or more input(s) blank')
            return redirect(url_for("trade_home.trade"))
        
    return render_template('trade.html', form=tradeForm, history_list=history_list)

def add_data(form_data):
    global history_list
    history_list.append(form_data)

def submit_order(form_data):
    global history_list
    global my_alert
    history_list.append(form_data)
    
    aliceBlue = OAuth2Session(application.config['CLIENT_ID'], token=session['oauth_token'])
    data = {'exchange':'NSE',
            'order_type': str(history_list[0]['order_type']),
            'instrument_token': str(history_list[0]['instrument_token']),
            'quantity': str(history_list[0]['quantity']),
            'disclosed_quantity':'0',
            'price' : str(history_list[0]['price']),
            'transaction_type': str(history_list[0]['product_type']) ,
            'trigger_price':'0',
            'validity':'DAY',
            'product': str(history_list[0]['flag']),
            'source':'web',
            'order_tag': 'single_order'
    }
    r = aliceBlue.post("https://ant.aliceblueonline.com/api/v2/order", json=data)
    print("response=" + str(r.json()))
    flash(u'Single order placed successfully')

def submit_orders(form_data):
    global history_list
    global order_list
    global my_alert
    history_list.append(form_data)
    for i in range(len(history_list)):
        data = {'exchange':'NSE',
            'order_type': str(history_list[i]['order_type']),
            'instrument_token': int(history_list[i]['instrument_token']),
            'quantity': int(history_list[i]['quantity']),
            'disclosed_quantity': 0,
            'price' : float(history_list[i]['price']),
            'transaction_type': str(history_list[i]['product_type']) ,
            'trigger_price': 0,
            'validity':'DAY',
            'product': str(history_list[i]['flag']),
        }
        order_list.append(data)
    
    aliceBlue = OAuth2Session(application.config['CLIENT_ID'], token=session['oauth_token'])
    final_data = {'source':'web',
                  'orders': order_list
                }
    r = aliceBlue.post("https://ant.aliceblueonline.com/api/v2/basketorder", json=final_data)
    print("response=" + str(r.json()))
    flash(u'Bulk order placed successfully')
