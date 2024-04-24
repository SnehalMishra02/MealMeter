from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, FloatField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.utils import secure_filename

class Main_Form(FlaskForm):
    weight = FloatField('Enter Your Weight')
    calorie = IntegerField('Calorie Target')
    submit = SubmitField("Cook Meal")