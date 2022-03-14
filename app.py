from flask import Flask, render_template, request, session

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/menu')
def menu():
    products = [
        ["Flat white", "Definitely created in New Zealand (not in the West Island) - a classic.", "180mL", "flatwhite",
         "4.00"],
        ["Latte", "The New Zealand latte is larger than a flat white and has more foamy milk.", "240mL", "latte",
         "4.00"],
        ["Espresso", "Straight from the machine, 60mL", "including crema.", "60mL", "espresso", "3.00"],
        ["Long black", "Hot water + espresso. 120mL.", "90mL", "longblack", "3.00"]]
    return render_template("menu.html", products=products)


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/login')
def login():
    return render_template("login.html")


app.run(host='0.0.0.0')
