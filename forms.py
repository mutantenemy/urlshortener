from flask import Flask, escape, request, render_template, url_for, redirect # Flask tools
from flask_wtf import FlaskForm # Enable Flask Forms
from wtforms import StringField, SubmitField # What kind of forms elements I need
from wtforms.validators import DataRequired, Length, URL, HostnameValidation # Which Validations methods I'll use

class Transform(FlaskForm):
    url = StringField('URL to transform',
                        validators = [DataRequired(), URL(False)]) # String field is has content that is an URL
    submit = SubmitField('Transform')