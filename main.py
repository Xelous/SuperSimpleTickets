from flask import Flask, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import render_template
import mysql.connector
import gc
import html
import datetime
from flask import flash

import DatabaseOperations

# The main flask application
g_FlaskApplication = Flask(__name__)

# flask-login
login_manager = LoginManager()
login_manager.init_app(g_FlaskApplication)
login_manager.login_view = "Login"

# Some protected url
@g_FlaskApplication.route('/')
@login_required
def home():
	l_user = current_user.get_id()
	if l_user != None:
		return Response("Hello World!")
	else:
		return ShowTickets()

# Login route
@g_FlaskApplication.route("/login", methods=["GET", "POST"])
def Login():
	if request.method == 'POST':
		l_username = request.form['Username']
		l_password = request.form['Password']
		l_User = DatabaseOperations.ValidateUser(l_username, l_password)
		if l_User != None:
			login_user(l_User, remember = True)
			return ShowTickets()
		else:
			return render_template('loginform.html', error = 'Failed to login')
	else:
		return render_template('loginform.html')

@g_FlaskApplication.route("/createticket", methods=["POST"])
@login_required
def CreateTicket():
	l_user = current_user.get_id()
	if l_user != None:
		if request.method == 'POST':
			l_area = request.form['Area']
			l_description = request.form['Description']
			DatabaseOperations.CreateTicket(l_area, l_description)
			return ShowTickets()
		else:
			return render_template("loginform.html", error ="Sorry you may only post tickets to this page")	
	else:
		return render_template("loginform.html", error ="Sorry only valid users may create a ticket")

# Add a ticket to the system
@g_FlaskApplication.route("/addticket")
@login_required
def AddTicket():
	l_user = current_user.get_id()
	if l_user != None:
		global g_FlaskApplication
		return g_FlaskApplication.send_static_file("addticket.html")
	else:
		return render_template("loginform.html", error ="Sorry only valid users may add a ticket")

# Show the tickets
@g_FlaskApplication.route("/tickets")
@login_required
def ShowTickets():
	l_user = current_user.get_id()
	if l_user != None:
		l_Tickets = DatabaseOperations.LoadTickets()
		l_DisplayTickets = []
		for l_Ticket in l_Tickets:
			l_DateAdded = l_Ticket[2].strftime('%Y-%m-%d %H:%M:%S')
			l_Description = l_Ticket[7]
			l_Id = str(l_Ticket[0])
			l_Resolved = l_Ticket[3]
			l_CurrentTicket = [ l_Id, l_Description, l_DateAdded, l_Resolved ]
			l_DisplayTickets.append(l_CurrentTicket)
		return render_template('tickets.html', tickets = l_DisplayTickets)
	else:
		return render_template("loginform.html", error = "Sorry Only valid users may view the ticket system")

# View specific Ticket
@g_FlaskApplication.route("/viewticket", methods=["POST"])
@login_required
def ViewTicket():
	l_user = current_user.get_id()
	if l_user != None:
		if request.method == "POST":
			l_TicketId = request.form["TicketId"]
			l_Ticket = DatabaseOperations.LoadTicket(l_TicketId)
			if l_Ticket != None:
				return render_template("viewticket.html", ticket = l_Ticket)
			else:
				return Response("Error Ticket Not Found")
		return Response("Error Viewing Ticket")
	else:
		return render_template("loginform.html", error = "Sorry only valid users may view tickets")

# Modify Ticket
@g_FlaskApplication.route("/modifyticket", methods=["POST"])
@login_required
def ModifyTicket():
	l_user = current_user.get_id()
	if l_user != None:
		if request.method == "POST":
			l_TicketId = request.form["TicketId"]
			l_Modification = request.form["Modification"]
			DatabaseOperations.ModifyTicket(l_TicketId, l_Modification)
			return ViewTicket()
		else:
			return render_template("loginform.html", error = "Sorry you may not directly modify a ticket")
	else:
		return render_template("loginform.html", error = "Sorry only valid users may modify tickets")


# Add Note to Ticket
@g_FlaskApplication.route("/addnote", methods=["POST"])
@login_required
def AddNote():
	l_user = current_user.get_id()
	if l_user != None:
		if request.method == "POST":
			l_TicketId = request.form["TicketId"]
			l_Note = request.form["notetext"]
			l_ByUser = current_user.Username
			DatabaseOperations.AddNoteToTicket(l_TicketId, l_Note, l_ByUser)
			return ViewTicket()
	else:
		return render_template("loginform.html", error = "Sorry only valid users may add notes to tickets")


# Callback to reload the user object
@login_manager.user_loader
def load_user(p_UserId):
	return DatabaseOperations.LoadUserByName(p_UserId)


# Generates a secret key for use in the system login
def GenerateSecretKey():
	import os
	l_key = os.urandom(24)
	return str(l_key)


# -- MAIN entry point --
if __name__ == "__main__":
	if not DatabaseOperations.DatabaseExists():
		print ("Creating Tickets database on localhost")
		DatabaseOperations.CreateDatabase()
	else:
		print ("Ticket database found")

	if DatabaseOperations.DatabaseExists():
		g_FlaskApplication.secret_key = GenerateSecretKey()
		g_FlaskApplication.run(host='0.0.0.0', debug=True)
	else:
		print ("Sorry, the ticket database has not been found on localhost")

