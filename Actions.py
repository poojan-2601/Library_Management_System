from calendar import day_abbr
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min = 2,max = 20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Sign up')

class AddBooks(FlaskForm):
    bookname = StringField('Book Name',validators=[DataRequired(),Length(min = 2,max = 50)])
    author = StringField('Author of the Book',validators=[DataRequired()])
    book_rent = IntegerField('Book rent',validators=[DataRequired(),NumberRange(min = 5,max = 50)])
    quantity = IntegerField('Quantity',validators=[DataRequired(),NumberRange(min = 1,max = 50)])
    submit = SubmitField('Add Book')

class Issue_Book_Form(FlaskForm):
    book_id = IntegerField('Book ID',validators=[DataRequired()])
    member_id = IntegerField('Member ID',validators=[DataRequired()])
    submit = SubmitField('Issue Book')

class Return_Book_Form(FlaskForm):
    transaction_id = IntegerField('Transaction id',validators=[DataRequired(),NumberRange(min=1)])
    amount_paid = IntegerField('Amount',validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Issue Book')

