from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator

# https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3

class AddVideoForm(FlaskForm):
    video_title = StringField('Video Title', validators=[DataRequired(), Length(min=2, max=20)])
    video_url = URLField('Video URL', validators=[DataRequired()])
    primaryselect = SelectField('Primary', choices=[])
    secondaryselect = SelectField('Secondary', choices=[])
    tertiaryselect = SelectField('Tertiary', choices=[])
    videosubmitbutton = SubmitField('Add Video')

class AddCategoryForm(FlaskForm):
    categoryname = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=20)])
    primarybool = BooleanField('Check if Primary Category')
    primaryselect = SelectField('Primary', choices=[])
    secondarybool = BooleanField('Check if Subcategory')
    secondaryselect = SelectField('Secondary', choices=[])
    addbutton = SubmitField('Add Category')

class AdvancedSearchForm(FlaskForm):
    searchterm = StringField('Search Term')
    primaryselect = SelectField('Primary', choices=[])
    secondaryfilterbool = BooleanField('Use Secondary Filter')
    secondaryselect = SelectField('Secondary', choices=[])
    tertiaryfilterbool = BooleanField('Use Tertiary Filter')
    tertiaryselect = SelectField('Tertiary', choices=[])
    advancedsearchbutton = SubmitField('Search')

class IndexSearchBar(FlaskForm):
    searchterm = StringField('Search Term')
