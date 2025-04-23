from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MessageForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    message = StringField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Submit')