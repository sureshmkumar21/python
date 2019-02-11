
from wtforms import Form, StringField

class TradeForm(Form):
    flag      = StringField("Flag")
    instrument_token  = StringField("Instrument Token")
    quantity      = StringField("Quantity")
    product_type      = StringField("Type")
    order_type      = StringField("Order Type")
    price      = StringField("Price")
#     price      = StringField("Price:", validators=[DataRequired()])
    
