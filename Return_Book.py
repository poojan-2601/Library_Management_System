from calendar import day_abbr
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo, NumberRange

class Return_Book_Form(FlaskForm):
    transaction_id = IntegerField('Transaction id',validators=[DataRequired(),NumberRange(min=1)])
    amount_paid = IntegerField('Amount',validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Issue Book')

