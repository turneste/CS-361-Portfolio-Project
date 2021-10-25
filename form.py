from wtforms import SubmitField, BooleanField, StringField, validators
from flask_wtf import Form
class RegForm(Form):
  name_first = StringField('First Name', 
                 [validators.DataRequired()])
  name_last = StringField('Last Name', 
                 [validators.DataRequired()])

  submit = SubmitField('Submit')