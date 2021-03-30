from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UploadMapForm(FlaskForm):
    mapname = StringField('Mapname', validators=[DataRequired()])
    routes = TextAreaField('Routes', validators=[DataRequired()])
    submit = SubmitField('Upload')
