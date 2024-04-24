from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class Text_form(FlaskForm):
    text_input = StringField('Text Input')
    submit = SubmitField("Submit")