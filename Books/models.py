import email
from email.policy import default
from unicodedata import name
from Books import db
from datetime import date


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    book_name = db.Column(db.String(length=30), nullable=False)
    author = db.Column(db.String(length=30), nullable=False)
    book_charge = db.Column(db.Integer(),nullable = False)
    quantity = db.Column(db.Integer(),nullable = False)
    def __init__(self,book_name,author,book_charge,quantity):
        self.book_name = book_name
        self.author = author
        self.book_charge = book_charge
        self.quantity = quantity
    

class Member(db.Model):
    memberid = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=30), nullable=False)
    debt = db.Column(db.Integer(), default = 0,nullable = False)
    def __init__(self,name,email):
        self.name = name
        self.email = email
    

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    book_id = db.Column(db.Integer(),db.ForeignKey('book.id'),nullable = False)
    book_name = db.Column(db.String(length=30), nullable=False)
    member_id = db.Column(db.Integer(),db.ForeignKey('member.memberid'),nullable = False)
    member_name = db.Column(db.String(length=30), nullable=False)
    per_day_fees = db.Column(db.Integer(),nullable = False)
    issue_date = db.Column(db.Date,nullable=False,default = date.today())
    return_date = db.Column(db.Date,nullable=True)
    total_charge = db.Column(db.Integer(),nullable = True)
    amount_paid = db.Column(db.Integer(),nullable = True)
    book_status = db.Column(db.Boolean(),nullable = False,default = False)
    def __init__(self,book_id,member_id,book_name,member_name,perDayFee):
        self.book_id = book_id
        self.member_id = member_id
        self.book_name = book_name
        self.member_name = member_name
        self.per_day_fees = perDayFee
        
