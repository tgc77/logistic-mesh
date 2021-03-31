from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UploadMapForm(FlaskForm):
    mapname = StringField('Mapname', validators=[DataRequired()])
    routes = TextAreaField('Routes', validators=[DataRequired()])
    submit = SubmitField('Upload')


class FindBestRouteForm(FlaskForm):
    mapname = StringField('Mapname', validators=[DataRequired()])
    origin = StringField('Origin', validators=[DataRequired()])
    destiny = StringField('Destiny', validators=[DataRequired()])
    truck_autonomy = StringField('TruckAutonomy', validators=[DataRequired()])
    liter_fuel_value = StringField(
        'LiterFuelValue', validators=[DataRequired()])
    submit = SubmitField('Find')
