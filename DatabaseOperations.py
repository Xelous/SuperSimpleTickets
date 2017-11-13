import datetime
import mysql.connector
from User import *

g_SQLDBUser = "root"
g_SQLDBPass = "root"
g_SQLDBName = "sst"
g_Connection = None

# Create database
def CreateDatabase():
	global g_SQLDBUser
	global g_SQLDBPass
	global g_SQLDBName
	l_Connection = mysql.connector.connect(
		user = g_SQLDBUser,
		password = g_SQLDBPass,
		host="localhost")
	if l_Connection != None:
		l_SQL = ("CREATE DATABASE IF NOT EXISTS " + g_SQLDBName)
		l_Cursor = l_Connection.cursor()
		l_Cursor.execute(l_SQL)
		l_Connection.commit()
		l_Cursor.close()
		l_Connection.close()
	l_Connection = SetupDB()
	if l_Connection != None:
		l_SQL = ("CREATE TABLE IF NOT EXISTS Tickets (TicketNumber INT PRIMARY KEY AUTO_INCREMENT, Area TEXT, DateAdded DATETIME, DateResolved DATETIME, Tested DATETIME, Completed DATETIME, Notes TEXT, Description TEXT)")
		l_Cursor = l_Connection.cursor()
		l_Cursor.execute(l_SQL)
		l_SQL = ("CREATE TABLE IF NOT EXISTS Users (Id INT PRIMARY KEY AUTO_INCREMENT, Username TEXT, Password TEXT)")
		l_Cursor.execute(l_SQL)
		l_SQL = ("INSERT INTO Users(Username, Password) VALUES ('admin', 'admin')")
		l_Cursor.execute(l_SQL)
		l_Connection.commit()
		l_Cursor.close()
		l_Connection.close()

# Check Database Exists
def DatabaseExists():
	l_result = False
	global g_SQLDBUser
	global g_SQLDBPass
	global g_SQLDBName
	l_Connection = mysql.connector.connect(
		user=g_SQLDBUser,
		password=g_SQLDBPass,
		host="localhost")
	if l_Connection != None:
		l_SQL = ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + g_SQLDBName + "'")
		l_Cursor = l_Connection.cursor()
		l_Cursor.execute(l_SQL)
		l_Data = l_Cursor.fetchall()
		if len(l_Data) > 0:
			if l_Data[0][0] == g_SQLDBName:
				l_result = True
		l_Cursor.close()
		l_Connection.close()
	return l_result

# Set the database up
def SetupDB():
	global g_SQLDBUser
	global g_SQLDBPass
	global g_SQLDBName
	global g_Connection
	if g_Connection == None:
    		g_Connection = mysql.connector.connect(
        		user=g_SQLDBUser,
       			password=g_SQLDBPass,
			host='localhost',
			database=g_SQLDBName)
	return g_Connection


# Validate a user
def ValidateUser(p_Username, p_Password):
	l_result = None
	l_SQL = ("SELECT Id FROM Users WHERE Username = '" + p_Username + "' AND Password = '" + p_Password + "'")
	l_DB = SetupDB()
	if l_DB != None:
		l_Cursor = l_DB.cursor()
		l_Cursor.execute(l_SQL)
		l_Data = l_Cursor.fetchall()
		if l_Data != None:
			if len(l_Data) == 1:
				l_result = User(l_Data[0][0], p_Username, p_Password)
			else:
				print ("Unknown result in SQL [2]")
		else:
			print ("Unknown result in SQL [1]")
		l_Cursor.close()
	else:
		print ("No database available");
	return l_result


# Load user by name
def LoadUserByName(p_Username):
	l_result = None
	l_SQL = ("SELECT * from Users WHERE Username = '" + p_Username + "'")
	l_DB = SetupDB()
	if l_DB != None:
		l_Cursor = l_DB.cursor()
		l_Cursor.execute(l_SQL)
		l_Data = l_Cursor.fetchall()
		if l_Data != None:
			if len(l_Data) == 1:
				l_result = User(l_Data[0][0], l_Data[0][1], l_Data[0][2])
			else:
				print ("Unknown user [" + p_Username + "]")
		else:
			print ("Unknown SQL result [3]")
		l_Cursor.close()
	else:
		print ("No database available!")
	return l_result

# Add a note to a ticklet
def AddNoteToTicket(p_TicketId, p_Note, p_ByUser):
	l_GetNotes = LoadTicket(p_TicketId)[6]
	if l_GetNotes == None:
		l_GetNotes = ""
	l_TotalNotes = l_GetNotes + "\r\n" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (" + p_ByUser + ") => " + p_Note
	l_SQL = ("UPDATE Tickets SET Notes = '" + l_TotalNotes + "' WHERE TicketNUmber = " + p_TicketId)
	l_DB = SetupDB()
	if l_DB != None:
		l_Cursor = l_DB.cursor()
		l_Cursor.execute(l_SQL)
		l_Cursor.close()
		l_DB.commit()

# Modify a ticket statuis
def ModifyTicket(p_TicketId, p_Modification):
	print ("Modding Ticket: " + p_TicketId + " : " + p_Modification)
	l_SQL = None
	if p_Modification == "0":
		l_SQL = ("UPDATE Tickets SET DateResolved = NOW() WHERE TicketNumber = " + p_TicketId)
	elif p_Modification == "1":
		l_SQL = ("UPDATE Tickets SET Tested = NOW() WHERE TicketNumber = " + p_TicketId)
	elif p_Modification == "2":
		l_SQL = ("UPDATE Tickets SET Completed = NOW() WHERE TicketNumber = " + p_TicketId)
	if l_SQL != None:
		print (l_SQL)
		l_DB = SetupDB()
		if l_DB != None:
			l_Cursor = l_DB.cursor()
			l_Cursor.execute(l_SQL)
			l_Cursor.close()
			l_DB.commit()


# Load Specific Ticket
def LoadTicket(p_TicketId):
	l_result = None
	l_SQL = ("SELECT * FROM Tickets WHERE TicketNumber = " + p_TicketId)
	l_DB = SetupDB()
	if l_DB != None:
		l_Cursor = l_DB.cursor()
		l_Cursor.execute(l_SQL);
		l_Data = l_Cursor.fetchall()
		if l_Data != None:
			l_result = l_Data[0]
		else:
			print ("Unknown Ticket Query [7]")
	else:
		print ("No database Available!")
	return l_result

# Load tickets
def LoadTickets():
	l_result = None
	l_SQL = ("SELECT * FROM Tickets")
	l_DB = SetupDB()
	if l_DB != None:
		l_Cursor = l_DB.cursor()
		l_Cursor.execute(l_SQL)
		l_Data = l_Cursor.fetchall()
		if l_Data != None:
			l_result = l_Data
		else:
			print ("Unknown Ticket Query [4]")
	else:
		print ("No database available!")
	return l_result


# Create a new ticket
def CreateTicket(p_Area, p_Description):
	l_SQL = ("INSERT INTO Tickets(Area,Description,DateAdded) VALUES ('" + p_Area + "', '" + p_Description + "', NOW())")
	l_DB = SetupDB()
	if l_DB != None:
		l_Cursor = l_DB.cursor()
		l_Cursor.execute(l_SQL)
		l_DB.commit()
	else:
		print ("No database available!")
