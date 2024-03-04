from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, URL, ValidationError, Optional
from wtforms import StringField, ValidationError

class CupcakeForm(FlaskForm):
    flavor = StringField('Flavor', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=0, max=10, message='Rating must be between 0 and 10')])
    image = StringField('Image URL', validators=[Optional(), URL()])