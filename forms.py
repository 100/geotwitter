from flask.ext.wtf import Form
from wtforms import TextField, validators

class ZipcodeForm(Form):
    zipcode = TextField('zipcode', [validators.required(), validators.Length(min=5, max=5)])
    search = TextField('zipcode', [validators.required(), validators.Length(min=1, max=50)])
