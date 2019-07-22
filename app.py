from flask import Flask, request, render_template, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/contact_app"
mongo = PyMongo(app)

@app.route('/')
def index():
	contacts = mongo.db.contacts.find()
	return render_template("index.html", contacts=contacts)

@app.route('/addContact', methods=['GET', 'POST'])
def addContact():
	if request.method == 'POST':
		if request.form['name'] and request.form['phone'] and request.form['address']:
			data = {'name': request.form['name'], 
					'phone_no': request.form['phone'], 
					'address': request.form['address']}
			mongo.db.contacts.insert_one(data)
		return redirect(url_for('index'))
	else:
		return render_template("addContact.html")

@app.route('/editContact/<string:contact_id>', methods=['GET', 'POST'])
def editContact(contact_id):
	if request.method == 'POST':
		if request.form['name'] and request.form['phone'] and request.form['address']:
			data = {'name': request.form['name'], 
					'phone_no': request.form['phone'], 
					'address': request.form['address']}
			mongo.db.contacts.update({"_id": ObjectId(contact_id)}, data)
		return redirect(url_for('index'))
	else:
		contact = mongo.db.contacts.find_one({"_id": ObjectId(contact_id)})
		return render_template("editContact.html", contact=contact)

@app.route('/deleteContact/<string:contact_id>', methods=['DELETE'])
def deleteContact(contact_id):
	if request.method == 'DELETE':
		mongo.db.contacts.remove({"_id": ObjectId(contact_id)})
	return '',204