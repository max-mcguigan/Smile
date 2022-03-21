from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error

DB_NAME = 'smile.db'

app = Flask(__name__)
app.secret_key = "hj32g4yds87dywqhej23e42378ry32890ey12983yw1h3h12iu3h21381293"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/menu')
def menu():
    con = create_connection(DB_NAME)
    query = "SELECT name, description, volume, price, image FROM product"
    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()
    return render_template("menu.html", products=product_list)


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        query = """SELECT id, fname, password FROM customer WHERE email = ?"""
        con = create_connection(DB_NAME)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()

        try:
            userid = user_data[0][0]
            firstname = user_data[0][1]
            db_password = user_data[0][2]
        except IndexError:
            return redirect('/login?error=email+invalid+or+password+incorrect')

        if db_password != password:
            return redirect('/login?error=email+invalid+or+password+incorrect')

        session['email'] = email
        session['userid'] = userid
        session['firstname'] = firstname
        print(session)
    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        print(request.form)
        fname = request.form.get("fname").strip().title()
        lname = request.form.get("lname").strip().title()
        email = request.form.get("email").strip().lower()
        password = request.form.get("pass")
        password2 = request.form.get("pass2")

        if password != password2:
            return redirect('/signup?error=Passwords+dont+match')

        con = create_connection(DB_NAME)
        query = "INSERT INTO customer(id, fname, lname, email, password) VALUES(NULL,?,?,?,?)"
        cur = con.cursor()
        try:
            cur.execute(query, (fname, lname, email, password))
        except sqlite3.IntegrityError:
            return redirect('/signup?error=email+is+already+used')
        con.commit()
        con.close()
        return redirect('/login')

    return render_template("signup.html")


@app.route('/logout')
def logout():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/?message=see+you+next+time')


def is_logged_in():
    if session.get("email") is None:
        print("not logged in")
        return False
    else:
        print("logged in")
        return True


app.run(host='0.0.0.0')
