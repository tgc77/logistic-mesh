from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectField,
    FloatField
)
from wtforms.validators import DataRequired


class UploadMapForm(FlaskForm):
    mapname = StringField('Mapname', validators=[DataRequired()])
    routes = TextAreaField('Routes', validators=[DataRequired()])
    submit = SubmitField('Upload')


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))


class FindBestRouteForm(FlaskForm):
    mapname = SelectField('Mapname', validators=[DataRequired()], coerce=str)
    origin = StringField('Origin', validators=[DataRequired()])
    destiny = StringField('Destiny', validators=[DataRequired()])
    truck_autonomy = MyFloatField(
        'Truck Autonomy', validators=[DataRequired()])
    liter_fuel_value = MyFloatField(
        'Liter Fuel Value', validators=[DataRequired()])
    submit = SubmitField('Find')
