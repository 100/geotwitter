from flask.ext.wtf import Form
from wtforms import TextField, validators

class ZipcodeForm(Form):
    zipcode = TextField('zipcode', [validators.required(), validators.Length(min=5, max=5)])
