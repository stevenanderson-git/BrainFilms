from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator

# https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3

class CategoryForm(FlaskForm):
    primary = SelectField('Primary', choices=[])
    secondary = SelectField('Secondary', choices=[])
    tertiary = SelectField('Tertiary', choices=[])

class AddCategoryForm(FlaskForm):
    categoryname = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=20)])
    primarybool = BooleanField('Check if Primary Category')
    primaryselect = SelectField('Primary', choices=[])
    secondarybool = BooleanField('Check if Subcategory')
    secondaryselect = SelectField('Secondary', choices=[])
    addbutton = SubmitField('Add Category')