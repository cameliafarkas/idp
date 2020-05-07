from flask import Flask, render_template, redirect, url_for
from flask import request
import requests
import copy
import random
import string
import mysql.connector

app = Flask(__name__)

user = ""

backend = "http://backend:4000/"
payment = "http://payment:4005/"

@app.route('/')
def index():
    global user
    end = ""
    if user == "":
        end = "login"
    else:
        end = "products"


    return render_template("index.html", end=end)

@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_post():
    global user
    name = request.form['username']
    passw = request.form['password']
    if name != "" and passw != "":
        user = name

        params = {"user" : user}
        url = backend + "set_shopping_cart"

        r = requests.post(url, data=params)

        return redirect(url_for('get_products'))
    return render_template("login.html")


@app.route('/products', methods=["GET"])
def get_products():
    global user

    if user == "":
        return redirect(url_for('login'))

    url = backend + "get_products"
    r = requests.get(url)

    data = r.json() 

    return render_template("products.html", products=data["products"])

@app.route('/products', methods=["POST"])
def add_products():
    global user

    url = backend + "add_product"

    params = {"id" : request.form["addcart"]}

    r = requests.post(url, data=params)

    return redirect(url_for('get_products'))

@app.route('/shopping_cart', methods=["GET"])
def get_shopping_cart():
    global user

    if user == "":
        return redirect("http://localhost:5000/login")

    url = backend + "get_cart_items"

    r = requests.get(url)
    data = r.json() 
    products = data["products"]

    pr = {}
    total = 0

    for (id, name, type, in_stock, company, price) in products:
        if id not in pr:
            pr[id] = {"quantity" : 1, "name" : name, "price" : int(price)}
        else:
            pr[id]["quantity"] += 1
            pr[id]["price"] += int(price)
        total += int(price)

    #change 
    products = []

    for (id, p) in pr.items():
        products.append((id, str(p["quantity"]), p["name"], str(p["price"])))

    return render_template("cart_items.html", products=products, total=str(total))

@app.route('/pay', methods=["GET"])
def pay():
    global user

    if user == "":
        return redirect(url_for('login'))

    url = backend + "get_cart_items"

    r = requests.get(url)
    data = r.json() 
    products = data["products"]

    pr = {}
    total = 0

    for (id, name, type, in_stock, company, price) in products:
        if id not in pr:
            pr[id] = {"quantity" : 1, "name" : name, "price" : int(price)}
        else:
            pr[id]["quantity"] += 1
            pr[id]["price"] += int(price)
        total += int(price)

    products = []

    for (id, p) in pr.items():
        products.append((id, str(p["quantity"]), p["name"], str(p["price"])))

    url = backend + "get_shipment_price"
    
    r = requests.get(url)

    data = r.json()
    shipment = data['shipment']
    number = len(products)

    return render_template("pay.html", products=products, subtotal=total, shipment=shipment, total=total + shipment, number=number)

@app.route('/pay', methods=["POST"])
def add_payment():
    global user
    url = payment + "make_payment"

    data = copy.deepcopy(request.form.to_dict())
    data["user"] = user

    if not(len(data["cardnumber"]) == 16) and not(data["cardnumber"].isdigit()):
        return redirect("http://localhost:5000/pay")
    if not(len(data["expyear"]) == 4) and not(data["expyear"].isdigit()):
        return redirect("http://localhost:5000/pay")
    if not(len(data["cvv"]) == 3) and not(data["cvv"].isdigit()):
        return redirect("http://localhost:5000/pay")

    r = requests.post(url, data=data)

    url = backend + "update_stock"

    url = backend + "delete_cart"

    r = requests.get(url)

    user = ""

    return redirect(url_for('finished_purchase'))

    return r.text

@app.route('/finished_purchase', methods=["GET"])
def finished_purchase():
    return render_template("finished.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
