from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)

mysql = MySQLConnector('friendsdb')

@app.route('/')
def index():
    friends = mysql.fetch("SELECT * FROM friends")
    #print friends
    return render_template('index.html', friends=friends)

    
@app.route('/friends', methods=['POST']) #create a new friend
def create():
	print request.form['first_name']
	print request.form['last_name']
	print request.form['occupation']
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(request.form['first_name'], request.form['last_name'], request.form['occupation'])
	print query
	mysql.run_mysql_query(query)
	return redirect('/')


@app.route('/friends/<id>/edit') #display the edit friend page for the particular friend
def edit(id):
	print "The ID in display friend is:",id

	query = "SELECT * FROM friends where id = '{}'".format(id)
	theperson = mysql.fetch(query)

	print "here is theperson",theperson
	return render_template('edit.html', theperson=theperson, id=id)



@app.route('/friends/<id>',  methods=['POST']) #handle the update to the page that has been edited
def update(id):
	print "The ID in update is:",id

	if request.form['first_name'] == "":
		print "the string is empty"
	print "first_name is:",request.form['first_name']
	print "last_name is:",request.form['last_name']

	query = "UPDATE friends SET first_name = '{}', last_name='{}', occupation='{}' WHERE id ={}".format(request.form['first_name'], request.form['last_name'], request.form['occupation'],id) 
	print query
	mysql.run_mysql_query(query)
	return redirect('/')



@app.route('/friends/<id>/delete',  methods=['POST'])  #handle when the user hits delete 
def destroy(id):
	print "The ID in Delete is:",id

	query = "DELETE FROM friends WHERE id = '{}'".format(id)  
	print query
	mysql.run_mysql_query(query)

	return redirect('/')

app.run(debug=True)
