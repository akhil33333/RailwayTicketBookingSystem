import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import sqlite3 as sql
from detect import *


app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')




@app.route('/covid', methods=['POST', 'GET'])
def covid():
    if request.method == 'POST':
        if 'img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['img']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg'))
            # print('upload_image filename: ' + filename)
            r = check_covid()
            msg = "You Have uploaded invalid Image"
            if r == 1:
                msg = "Your Test Kit Image Says Covid Negative and allowed to book Ticket"
                return render_template('ticket.html', msg=msg)
            if r == 2:
                msg = "Your Test Kit Image says Covid Positive and not allowed to Book Ticket"

            print('Image successfully uploaded and displayed below')
            return render_template('result.html', msg=msg)
        else:
            print('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        return render_template('covid.html')


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    msg = ''
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zipcode = request.form['zipcode']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (firstname,lastname,email,phone,address,city,state,zipcode) VALUES(?,"
                            "?,?,?,?,?,?,?)", (firstname, lastname, email, phone, address, city, state, zipcode))

                con.commit()
                msg = "added user successfully"

        except:
            con.rollback()
            msg = "error in insert user operation"

        finally:
            return render_template('covid.html')
            con.close()


@app.route('/book_ticket', methods=['POST', 'GET'])
def book_ticket():
    msg = ''
    if request.method == 'POST':
        try:
            from_place = request.form['from_place']
            to_place = request.form['to_place']
            persons = request.form['persons']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO tickets (from_place,to_place,persons) VALUES(?,?,?)", (from_place, to_place, persons))

                con.commit()
                msg = "ticket booked successfully"

        except:
            con.rollback()
            msg = "error in insert user operation"

        finally:
            return render_template('result.html', msg=msg)
            con.close()


if __name__ == '__main__':
    app.run(debug=True)
