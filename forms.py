from flask import Flask, escape # Flask tools
from flask_wtf import FlaskForm # Enable Flask Forms
from wtforms import StringField, SubmitField # What kind of forms elements I need
from wtforms.validators import DataRequired, Length, URL # Which Validations methods I'll use

class Transform(FlaskForm):
    url = StringField('URL to transform',
                        validators = [DataRequired(), URL(False, message='The URL was invalid. Use HTTP://yourURL.com/moreinfo')]) # String field is has content that is an URL
    submit = SubmitField('Transform')
    remove = SubmitField('Remove')