from starlette_wtf import StarletteForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField,SelectField,DateTimeField,TimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo



class TrainForm(StarletteForm):
    #crud=SelectField("Add/Update/Delete:Train",choices=['Add','Update','Delete'])
    number=StringField("Train number",validators=[DataRequired(), ],render_kw={'readonly': False})
    name=StringField("Train name",validators=[DataRequired(), ])
    type=StringField("Train type",validators=[DataRequired(), ])
    initial_station_code=StringField("Initial station code",validators=[DataRequired(), ])
    final_station_code=StringField("Final station code",validators=[DataRequired(), ])
    departure_time=TimeField("Initial departure time(hh:mm:ss)",validators=[DataRequired(), ])
    arrival_time=TimeField("Final arriving time(hh:mm:ss)",validators=[DataRequired(), ])
    duration=StringField("Duration(X hrs Y mins)",validators=[DataRequired(), ])
    distance=IntegerField("Distance",validators=[DataRequired(), ])
    first_class=BooleanField("First class")
    chair_car=BooleanField("Chair car")
    first_ac=BooleanField("First ac")
    second_ac=BooleanField("Second ac")
    third_ac=BooleanField("Third ac")
    sleeper=BooleanField("Sleeper")
    submit = SubmitField('Submit')

class StationForm(StarletteForm):
    #crud=SelectField("Add/Update/Delete:Train",choices=['Add','Update','Delete'])
    code=StringField("Station code",validators=[DataRequired(), ],render_kw={'readonly': False})
    name=StringField("Station name",validators=[DataRequired(), ])
    zone=StringField("Station zone",validators=[DataRequired(), ])
    address=StringField("Station address",validators=[DataRequired(), ])
    state=StringField("State name",validators=[DataRequired(), ])
    coordinates=StringField("Coordinates(Longitude,Latitude)",validators=[DataRequired(),])
    submit = SubmitField('Submit')

class ScheduleForm(StarletteForm):
     #crud=SelectField("Add/Update/Delete:Train",choices=['Add','Update','Delete'])
     sc_id=IntegerField("Schedule id",validators=[DataRequired(), ],render_kw={'readonly': False})
     train_number=StringField("Train number",validators=[DataRequired(), ])
     station_code=StringField("Station code",validators=[DataRequired(), ])
     departure_time=TimeField("Departure time(hh:mm:ss)",validators=[DataRequired(), ])
     arrival_time=TimeField("Arrival time(hh:mm:ss)",validators=[DataRequired(), ])
     day_of_travel=IntegerField("Day of travel",validators=[DataRequired(), ])
     submit = SubmitField('Submit')