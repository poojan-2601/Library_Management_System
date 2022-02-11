from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo, NumberRange

class AddBooks(FlaskForm):
    bookname = StringField('Book Name',validators=[DataRequired(),Length(min = 2,max = 50)])
    author = StringField('Author of the Book',validators=[DataRequired()])
    book_rent = IntegerField('Book rent',validators=[DataRequired(),NumberRange(min = 5,max = 50)])
    quantity = IntegerField('Quantity',validators=[DataRequired(),NumberRange(min = 1,max = 50)])
    submit = SubmitField('Add Book')

