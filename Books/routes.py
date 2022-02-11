from crypt import methods
from flask import Flask, render_template, url_for,flash,redirect
from Return_Book import Return_Book_Form
from add_books import AddBooks
from form import RegistrationForm
from Books import models,db,app
from random import randint
from Issue_Book import Issue_Book_Form
from datetime import date
import requests


@app.route("/")
@app.route("/home")
def home():
    member_data = models.Member.query.all()
    transaction_details = models.Transaction.query.all()
    return render_template('home.html',posts = member_data,transaction = transaction_details)


@app.route("/library")
def library():
    book_data = models.Book.query.all()
    transcation_data = models.Transaction.query.all()
    return render_template('library.html',title='library',books = book_data,transcation_data = transcation_data)

@app.route("/register",methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        member = models.Member(form.username.data,form.email.data)
        db.session.add(member)
        db.session.commit()
        flash(f'member added succesfully {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register',form = form)

@app.route("/Issue_Book",methods = ['GET','POST'])
def Issue_Book():
    action = ["update quantity","fetch from API"]
    issue_data = Issue_Book_Form()
    if issue_data.validate_on_submit():
        book = models.Book.query.filter_by(id = issue_data.book_id.data).first()
        member = models.Member.query.filter_by(memberid = issue_data.member_id.data).first()
        if book != None and member != None:
            per_day_charge = book.book_charge
            if book.quantity > 0:   
                transaction_data = models.Transaction(issue_data.book_id.data,issue_data.member_id.data,book.book_name,member.name,per_day_charge)
                book.quantity = book.quantity - 1
                db.session.add(transaction_data)
                db.session.commit()
                flash(f'{book.book_name} Issued successfully for {member.name}','success')
                return redirect(url_for('home'))
            else:
                flash(f'{book.book_name} is not in stock, kindly wait or issue another book!!!!','failure')
        else:
            flash(f'Please enter valid details!!!!!','failure')
    return render_template('Issue_Book.html',title = 'Issue Book',issue_data = issue_data)  

@app.route("/Return_Book",methods=['GET','POST'])
def Return_Book():
    return_data = Return_Book_Form()
    if return_data.validate_on_submit():
        transaction= models.Transaction.query.filter_by(transaction_id = return_data.transaction_id.data).first()
        member = models.Member.query.filter_by(memberid = transaction.member_id).first()
        book = models.Book.query.filter_by(id = transaction.book_id).first()
        days = (date.today() - transaction.issue_date).days
        if days == 0:
            total_charge = transaction.per_day_fees
        else:
            total_charge = days * transaction.per_day_fees
        outstanding_debt = member.debt
        if outstanding_debt - return_data.amount_paid.data + total_charge > 500:
            flash(f'Your current debt plus total charge exceeds 500 INR value, kindly pay an amount greater than or equal to {outstanding_debt + total_charge - 500}','failure')
            return redirect(url_for('Return_Book'))
        else:
            member.debt = member.debt - return_data.amount_paid.data + total_charge
            transaction.total_charge = total_charge
            transaction.amount_paid = return_data.amount_paid.data
            transaction.return_date = date.today()
        transaction.book_status = True
        book.quantity = book.quantity + 1
        flash(f"Book returned",'success')    
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('Return_Book.html',title = 'Return Book',return_data = return_data)

@app.route("/Import_Book",methods = ["GET","POST"])
def Import_Book():
    pass


@app.route("/add_books",methods = ['GET','POST'])
def add_books():
    book_data = AddBooks()
    if book_data.validate_on_submit():
        book = models.Book(book_data.bookname.data,book_data.author.data,book_data.book_rent.data,book_data.quantity.data)
        db.session.add(book)
        db.session.commit()
        flash(f'Book added successfully!!!!','success')
        return redirect(url_for('library'))
    return render_template('add_books.html', title='add_books',book_data = book_data)

