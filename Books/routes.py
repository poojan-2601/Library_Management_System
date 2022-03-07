from crypt import methods
from flask import Flask, render_template, url_for,flash,redirect
from sqlalchemy import null
from Books import models,db,app
from random import randint
from datetime import date
import requests
from Actions import RegistrationForm,AddBooks,Issue_Book_Form,Return_Book_Form,IncreaseQuantity,DeleteBook,DeleteMember


@app.route("/")
@app.route("/home")
def home():
    transaction_details = models.Transaction.query.all()
    return render_template('home.html',transaction = transaction_details)


@app.route("/library")
def library():
    book_data = models.Book.query.all()
    transcation_data = models.Transaction.query.all()
    return render_template('library.html',title='library',books = book_data,transcation_data = transcation_data)

@app.route("/Members")
def Members():
    member_data = models.Member.query.all()
    return render_template('Members.html',title='Members',member_data = member_data)


@app.route("/register",methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        member = models.Member(form.username.data,form.email.data)
        db.session.add(member)
        db.session.commit()
        flash(f'member added succesfully {form.username.data}!','success')
        return redirect(url_for('Members'))
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
                flash(f'{book.book_name} is not in stock, kindly wait or issue another book!!!!','danger')
        else:
            flash(f'Please enter valid details!!!!!','danger')
    return render_template('Issue_Book.html',title = 'Issue Book',issue_data = issue_data)  

@app.route("/Return_Book/<int:transactionId>",methods=['GET','POST'])
def Return_Book(transactionId):
    return_data = Return_Book_Form()
    if return_data.validate_on_submit():
        transaction= models.Transaction.query.filter_by(transaction_id = transactionId).first()
        member = models.Member.query.filter_by(memberid = transaction.member_id).first()
        book = models.Book.query.filter_by(id = transaction.book_id).first()
        days = (date.today() - transaction.issue_date).days
        if days == 0:
            total_charge = transaction.per_day_fees
        else:
            total_charge = days * transaction.per_day_fees
        outstanding_debt = member.debt
        if outstanding_debt - return_data.amount_paid.data + total_charge > 500:
            flash(f'Your current debt plus total charge exceeds 500 INR value, kindly pay an amount greater than or equal to {outstanding_debt + total_charge - 500}','danger')
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

@app.route("/Increase_Quantity",methods = ["GET","POST"])
def Increase_Quantity():
    book_information = IncreaseQuantity()
    if book_information.validate_on_submit():
        book = models.Book.query.filter_by(id = book_information.book_id.data).first()
        if book != None:
            book.quantity = book.quantity + book_information.quantity.data
            db.session.commit()
            flash(f'{book_information.quantity.data} added to {book.book_name}','success')
            return redirect(url_for('library'))
        else:
            flash(f'Please enter a valid book ID!!!!!','danger')
            return redirect(url_for('Increase_Quantity'))
    return render_template('Increase_Quantity.html',title = 'Increase Quantity',book_information = book_information)

@app.route("/Delete_Books",methods = ["GET","POST"])
def Delete_Books():
    book_information = DeleteBook()
    if book_information.validate_on_submit():
        book = models.Book.query.filter_by(id = book_information.book_id.data).first()
        if book != None:
            book_name = book.book_name
            book_id = book.id
            transaction = models.Transaction.query.filter_by(book_id = book_id).first()
            if transaction:
                print(transaction.book_status)
                if transaction.book_status == True:
                    db.session.delete(book)
                    db.session.commit()
                    return redirect(url_for('library'))
                else:
                    flash(f'This book is currently issued by {transaction.member_name}, kindly wait for them to return the book','danger')
                    return redirect(url_for('Delete_Books'))
            else:
                db.session.delete(book)
                db.session.commit()
                flash(f'{book_name} Deleted from Library','success')
                return redirect(url_for('library'))
        else:
            flash(f'Please enter a valid book ID!!!!!','danger')
            return redirect(url_for('Delete_Books'))
    return render_template('Delete_Books.html',title = 'Delete Books',book_information = book_information)

@app.route("/Delete_Member",methods = ["GET","POST"])
def Delete_Member():
    member_info = DeleteMember()
    if member_info.validate_on_submit():
        member = models.Member.query.filter_by(memberid = member_info.member_id.data).first()
        if member != None:
            member_name = member.name
            db.session.delete(member)
            db.session.commit()
            flash(f'{member_name} Removed from Library','success')
            return redirect(url_for('Members'))
        else:
            flash(f'Please enter a valid member ID!!!!!','danger')
            return redirect(url_for('Delete_Member'))
    return render_template('Delete_Member.html',title = 'Delete Member',member_info = member_info
    )



