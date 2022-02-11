from calendar import day_abbr
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo, NumberRange

class Issue_Book_Form(FlaskForm):
    book_id = IntegerField('Book ID',validators=[DataRequired()])
    member_id = IntegerField('Member ID',validators=[DataRequired()])
    submit = SubmitField('Issue Book')

