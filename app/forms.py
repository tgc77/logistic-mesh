from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class UploadMapForm(FlaskForm):
    mapname = StringField('Mapname', validators=[DataRequired()])
    routes = TextAreaField('Routes', validators=[DataRequired()])
    submit = SubmitField('Upload')


class FindBestRouteForm(FlaskForm):
    mapname = SelectField('Mapname', validators=[DataRequired()], coerce=str)
    origin = StringField('Origin', validators=[DataRequired()])
    destiny = StringField('Destiny', validators=[DataRequired()])
    truck_autonomy = StringField('Truck Autonomy', validators=[DataRequired()])
    liter_fuel_value = StringField(
        'Liter Fuel Value', validators=[DataRequired()])
    submit = SubmitField('Find')
