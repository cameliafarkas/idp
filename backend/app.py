from flask import Flask, render_template
from flask import request
import random
import string
import mysql.connector

app = Flask(__name__)

user = ""

frontend = "http://ec2-3-8-137-154.eu-west-2.compute.amazonaws.com:5000/"

mydb = mysql.connector.connect(
  host="database",
  user="root",
  passwd="root",
  database="hairshop"
)

mycursor = mydb.cursor()

@app.route('/set_shopping_cart', methods=["POST"])
def set_shopping_cart():
	global user
	user = request.form['user']
	query = "INSERT INTO shoppingcart (user) VALUES (%s)"

	try:
		mycursor.execute(query,(user,))
	except mysql.connector.Error:
		return "Adaugare cos esuata"

	mydb.commit()
	return "Cos adaugat"

@app.route('/get_products', methods=["GET"])
def get_products():
	products = []

	query = "SELECT * FROM product"

	try:
		mycursor.execute(query)
	except mysql.connector.Error:
		return "Afisare produse esuata"


	for value in mycursor.fetchall():
		products.append(value)

	result = {"products" : products}

	return result

@app.route('/add_product', methods=["POST"])
def add_product():
	global user
	id = request.form["id"]

	query = "SELECT quantity from stock where product_id= %s"

	try:
		mycursor.execute(query,(id,))
	except mysql.connector.Error:
		return "Produsul nu exista"

	data = mycursor.fetchone()

	if data[0] == 0:
		return "Nu exista stoc"

	query = "INSERT INTO cart_item (id_product, id_shoppingcart) VALUES (%s, %s)"
	val = (id, user)

	try:
		mycursor.execute(query, val)
	except mysql.connector.Error:
		return "Adaugare produs in cos esuata"

	mydb.commit()

	return "Produs adaugat in cos"

@app.route('/get_cart_items', methods=["GET"])
def get_cart_items():
	global user
	products = []

	query = "SELECT id_product FROM cart_item where id_shoppingcart=%s"

	try:
		mycursor.execute(query, (user,))
	except mysql.connector.Error:
		return "Afisare produse esuata"


	query = "SELECT * FROM product where id=%s"
	for value in mycursor.fetchall():
		try:
			mycursor.execute(query,(value[0],))
		except mysql.connector.Error:
			return "Produsul nu exista"

		data = mycursor.fetchone()
		products.append(data)


	result = {"products" : products}

	return result

@app.route('/get_shipment_price', methods=["GET"])
def get_shipment_price():
	global user

	query = "SELECT delivery_cost FROM shoppingcart WHERE user=%s"

	try:
		mycursor.execute(query, (user,))
	except mysql.connector.Error:
		return "Obtinere cost transport esuata"

	data = mycursor.fetchone()

	result = {"shipment" : data[0]}

	return result

@app.route('/update_stock', methods=["GET"])
def update_stock():
	global user
	products = []

	query = "SELECT id_product FROM cart_item where id_shoppingcart=%s"

	try:
		mycursor.execute(query, (user,))
	except mysql.connector.Error:
		return "Afisare produse esuata"


	query = "SELECT quantity FROM stock where product_id=%s"
	for value in mycursor.fetchall():
		try:
			mycursor.execute(query,(value[0],))
		except mysql.connector.Error:
			return "Obtinere stock esuata"

		data = mycursor.fetchone()
		products.append({"id" : value[0], "total_quantity" : data[0]})

	query = "SELECT id FROM cart_item WHERE id_shoppingcart=%s"

	for product in products:
		value = (user, product['id'])

		try:
			mycursor.execute(query, (user, ))
		except mysql.connector.Error:
			return "Obtinere numar produse esuata"

		number = len(mycursor.fetchall())

		query = "DELETE from stock where product_id=%s"

		try:
			mycursor.execute(query, (product["id"],))
		except mysql.connector.Error:
			return "Stergere esuata"

		mydb.commit()

		query = "INSERT INTO stock (quantity, product_id) VALUES (%s, %s)"
		value = (product["total_quantity"] - number, product["id"])

		try:
			mycursor.execute(query, value)
		except mysql.connector.Error:
			return "Adaugare esuata"


	return "UPDATE DONE"

@app.route('/delete_cart', methods=["GET"])
def delete_cart():
	global user
	query = "DELETE FROM shoppingcart WHERE user=%s"

	try:
		mycursor.execute(query, (user,))
	except mysql.connector.Error:
		return "Stergere cos esuata"

	mydb.commit()

	user = ""
	return "Stergere cos cu succes"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4000", debug=True)
