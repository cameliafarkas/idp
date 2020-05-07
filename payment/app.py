from flask import Flask, render_template
from flask import request
import random
import string
import mysql.connector

app = Flask(__name__)

frontend = "http://frontend:5000/"

mydb = mysql.connector.connect(
  host="database",
  user="root",
  passwd="root",
  database="hairshop"
)

mycursor = mydb.cursor()

@app.route('/make_payment', methods=["POST"])
def make_payment():
	data = request.form

	query = "INSERT INTO pay (cart_id, name, name_card, email, address, card_number, year, cvv, value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	value = (data["user"], data["name"], data["cardname"], \
		data["email"], data["address"], data["cardnumber"], data["expyear"], data["cvv"], data["value"])

	try:
		mycursor.execute(query, value)
	except mysql.connector.Error:
		return "Adaugare plata esuata"

	mydb.commit()

	return "Adaugare plata reusta"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4005", debug=True)