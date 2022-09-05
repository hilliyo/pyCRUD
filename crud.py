'''
=============================
Basic CRUD with Python
=============================
developed by: Gilberto Delgado
https://github.com/hilliyo/pyCRUD
Mail: iscgil64@gmail.com
Version: 1.0 (Linux)
Python Version: 3
Date: Aug. 30th, 2022

README:
This is a command-line-based program that inserts, modified,
reads and deletes information from a table in a database with MySQL.
Table have the next columns:
	
	MOVIES
_____________________
Columns    |  Type 
           |
id         | BIGINT
title      | VARCHAR
year       | SMALLINT

How to use?

1. Run script "db.sql" to create the database that works with this program.
   Do this with the following command:

   mysql -u root -p < db.sql

   Enter password and wait that process ends.

   WARNING! If you have a database with name "movies" this action will delete it.

2. Run file "crud.py" with the following command:
   
   python3 crud.py

3. Enjoy!

Report bugs and feedback: iscgil64@gmail.com

'''

from __future__ import print_function
from terminaltables import SingleTable
import pymysql
import os
import time

def get_connection():
	#this function returns the connection to the database
	try:
		connection = pymysql.connect(host = 'localhost',
			user = 'root',
			password = '',
			database = 'movies')
	except (pymysql.err.OperationalError, pymysql.InternalError) as e:
		print("Error...")
		print(e)
		
	finally:
		return connection

def get_all(type, data):
	#This function return the rows that results from a select query
	connection = get_connection()
	#create SingleTable object. See https://pypi.org/project/terminaltables/
	result_table = SingleTable((),"Hi")
	try:
		with connection.cursor() as cursor:
			#get all rows
			if type == 0:
				sentence = "SELECT * FROM movies;"
				cursor.execute(sentence)
				movies = cursor.fetchall()

				title = "Movies"
				#header of table
				data_table = [("ID", "Title", "Year")]
				#convert tuple in list
				movies = list(movies)
				#join both lists to form table content
				data_table.extend(movies)

				#set the result table value
				table_instance = SingleTable(data_table, title)
				result_table = table_instance.table
			
			#search by id
			elif type == 1:
				sentence = "SELECT * FROM movies WHERE id = %s;"
				cursor.execute(sentence, (data))
				movies = cursor.fetchall()

				title = "Movies"
				data_table = [("ID", "Title", "Year")]
				movies = list(movies)
				data_table.extend(movies)

				table_instance = SingleTable(data_table, title)
				result_table = table_instance.table
			
			#search by title
			elif type == 2:
				sentence = "SELECT * FROM movies WHERE title LIKE %s"
				#format string to sql query
				data = "%" + data + "%"
				cursor.execute(sentence, (data))
				movies = cursor.fetchall()

				title = "Movies"
				data_table = [("ID", "Title", "Year")]
				movies = list(movies)
				data_table.extend(movies)

				table_instance = SingleTable(data_table, title)
				result_table= table_instance.table
			
			#search by year
			elif type == 3:
				sentence = "SELECT * FROM movies WHERE year = %s"
				cursor.execute(sentence, (data))
				movies = cursor.fetchall()

				title = "Movies"
				data_table = [("ID", "Title", "Year")]
				movies = list(movies)
				data_table.extend(movies)

				table_instance = SingleTable(data_table, title)
				result_table = table_instance.table
			
			#search by title, id or year
			elif type == 4:
				string = "%" + str(data) + "%"
				sentence = "SELECT * FROM movies WHERE title LIKE %s OR id = %s OR year = %s"
				cursor.execute(sentence, (string, data, data))
				movies = cursor.fetchall()

				title = "Movies"
				data_table = [("ID", "Title", "Year")]
				movies = list(movies)
				data_table.extend(movies)

				table_instance = SingleTable(data_table, title)
				result_table = table_instance.table

			#get latest 20 records
			elif type == 5:
				sentence = "SELECT * FROM movies ORDER BY id ASC LIMIT 20;"
				cursor.execute(sentence)
				movies = cursor.fetchall()

				title = "Movies"
				data_table = [("ID", "Title", "Year")]
				movies = list(movies)
				data_table.extend(movies)

				table_instance = SingleTable(data_table, title)
				result_table = table_instance.table
	finally:
		connection.close()
	return result_table

def insert():
	#This function create new rows in database
	while True:
		os.system("clear")
		print("--- Latest records ----")
		print(get_all(5, ""))
		print("--- Register movies ---")
		print("Type 0 to Exit")
		title = input("Enter title: ")
		if title == "0":
			#Exit
			break
		year = input("Enter year: ")

		if year.isdigit():
			answer = input("Data is OK? [y/n]: ")

			if answer == "y":
				connection = get_connection()
				print("Writing data ...")
			
				try:
					with connection.cursor() as cursor:
						sentence = "INSERT INTO movies(title, year) VALUES (%s, %s);"
						cursor.execute(sentence, (title, year))
						connection.commit()
				finally:
					connection.close()

			elif answer == "n":
				print("Try again...")
		else:
			print("Invalid input!")
			time.sleep(2)

def update():
	#This function update database
	while True:
		os.system("clear")
		print("--- Latest records ---")
		print(get_all(5,""))
		connection = get_connection()
		print("--- Update data ---")
		print("Type 0 to Exit")
		movie_id = input("Type id to update: ")
		
		if movie_id == "0":
			#Exit
			break		
	
		print("Fields:")
		print("1. Title")
		print("2. Year")
		print("3. All")
		print("0. Exit")		
		choice = input("Enter option: ")

		if choice == "0":
			#Exit
			break

		#Update title
		elif choice == "1":
			new_title = input("Type new title: ")	
			try:
				with connection.cursor() as cursor:
					sentence = "UPDATE movies SET title = %s WHERE id = %s;"

					cursor.execute(sentence, (new_title, movie_id))
					connection.commit()
			finally:
				connection.close()

		#Update year
		elif choice == "2":
			new_year = input("Type new year: ")
			try:
				with connection.cursor() as cursor:
					sentence = "UPDATE movies SET year = %s WHERE id = %s;"

					cursor.execute(sentence, (new_year, movie_id))
					connection.commit()
			finally:
				connection.close()
		
		#Update both fields
		elif choice == "3":
			new_title = input("Type new title: ")
			new_year = input("Type new year: ")

			try:
				with connection.cursor() as cursor:
					sentence = "UPDATE movies SET title = %s, year = %s WHERE id = %s;"
					cursor.execute(sentence, (new_title, new_year, movie_id))
				connection.commit()
			finally:
				connection.close()

def read():
	#This functions get data by different parameters
	while True:
		os.system("clear")
		print("--- Latest records ---")
		#Print terminaltables
		print(get_all(5, ""))
		print()
		print("Options: ")
		print("1. Search by id.")
		print("2. Search by title.")
		print("3. Search by year.")
		print("4. Search.")
		print("0. Exit")

		choice = input("Enter option: ")
		if choice.isdigit():
			if choice == "0":
				#Exit
				break

			#Search by id
			elif choice == "1":
				movie_id = input("Type id: ")
				#Print terminaltables
				print(get_all(1, movie_id))
				input("Press Enter to continue: ")

			#Search by title
			elif choice == "2":
				title_string = input("Type title: ")
				print(get_all(2, title_string))
				input("Press Enter to continue: ")

			#Search by year
			elif choice == "3":
				year = input("Type year: ")
				print(get_all(3,year))
				input("Press Enter to continue: ")

			#Search by title, year or id
			elif choice == "4":
				string = input("Type keyword: ")
				print(get_all(4, string))
				input("Press Enter to continue: ")
			else:
				print("Invalid option")
				time.sleep(2)
		else:
			print("Invalid input")
			time.sleep(2)

def delete():
	#This function delete rows in database
	while True:
		os.system("clear")
		print("--- Latest records ---")
		#Print terminaltables
		print(get_all(5, ""))
		print()
		print("Options: ")
		print("1. Delete by id.")
		print("2. Delete by title.")
		print("3. Delete by year.")
		print("4. Delete.")
		print("0. Exit")

		connection = get_connection()
		choice = input("Enter option: ")

		if choice == "0":
			#Exit
			break

		#Delete by id
		elif choice == "1":
			print("Type 0 to Exit")
			movie_id = input("Type id: ")
			if movie_id == "0":
				#Clean screen and Exit
				os.system("clear")
			else:
				try:
					with connection.cursor() as cursor:
						sentence =  "DELETE FROM movies WHERE id = %s;"
						answer = input("Delete? [y/n]: ")
						if answer == "y":
							print("Deleting...")
							cursor.execute(sentence, (movie_id))
							connection.commit()
						elif answer == "n":
							os.system("clear")
						else:
							print("Invalid option")
							time.sleep(2)
				except (pymysql.err.OperationalError, pymysql.InternalError) as e:
					print("ID not exist")
					time.sleep(2)
				finally:
					connection.close()

		#Delete by title
		elif choice == "2":
			print("Type 0 to Exit")
			title_string = input("Type title: ")
			if title_string == "0":
				#Clear screen and Exit
				os.system("clear")
			else:
				try:
					with connection.cursor() as cursor:
						sentence =  "DELETE FROM movies WHERE title = %s;"
						answer = input("Delete? [y/n]: ")
						if answer == "y":
							print("Deleting...")
							cursor.execute(sentence, (title_string))
							connection.commit()
						elif answer == "n":
							os.system("clear")
						else:
							print("Invalid option")
							time.sleep(3)
							break
				finally:
					connection.close()

		#Delete by year
		elif choice == "3":
			print("Type 0 to Exit")
			year = input("Type year: ")
			if year == "0":
				#Clear screen and Exit
				os.system("clear")
			elif not year.isdigit():
				print("Invalid input")
				time.sleep(2)
			else:
				try:
					with connection.cursor() as cursor:
						sentence =  "DELETE FROM movies WHERE year = %s;"
						print("WARNING! This will delete all rows that contains year = \"" + year + "\"")
						answer = input("Delete? [y/n]: ")
						if answer == "y":
							print("Deleting...")
							cursor.execute(sentence, (year))
							connection.commit()
						elif answer == "n":
							os.system("clear")
						else:
							print("Invalid option")
							time.sleep(2)
				except (pymysql.err.OperationalError, pymysql.InternalError) as e:
					print("Invalid input")
					time.sleep(2)
				finally:
					connection.close()
		
		#Delete by id, title or year
		elif choice == "4":
			print("Type 0 to Exit")
			string = input("Type id, title or year: ")
			#declaring variables
			year = 0
			movie_id = 0
			title = ""
			if string == "0":
				#Clear screen and Exit
				os.system("clear")
			else:
				#Set movie_id = 0 and year = 0 to prevent pymysql exception about data types
				if string.isdigit():
					year = int(string)
					movie_id = int(string)
					title = string
				else:
					title = string
					if movie_id == 0 or year == 0:
						print("Set id = " + str(movie_id) + "...")
						print("Set year = " + str(year) + "...")
				try:
					with connection.cursor() as cursor:
						#format string to sql query
						title_2 = "%" + title + "%"
						sentence =  "DELETE FROM movies WHERE year = %s OR title LIKE %s OR id = %s;"
						print("WARNING! This will delete all rows that contains \"" + title + "\" in Title field")
						print("WARNING! This will delete all rows with year = \"" + str(year) + "\"")
						print("WARNING! This will delete row with id = \"" + str(movie_id) + "\"")
						answer = input("Delete? [y/n]: ")
						if answer == "y":
							print("Deleting...")
							cursor.execute(sentence,(year, title_2, movie_id))
							connection.commit()
						elif answer == "n":
							#Clear screen and Exit
							os.system("clear")
						else:
							print("Invalid option")
							time.sleep(2)
				finally:
					connection.close()
		else:
			print("Invalid option")
			time.sleep(3)
			break

def menu():
	#This function show menu
	while True:
		os.system("clear")
		print("--- CRUD with Python ---")
		print("Options:")
		print("1. Insert data. ")
		print("2. Read data.")
		print("3. Update data. ")
		print("4. Delete data. ")
		print("0. Exit")

		choice = input("Your choice: ")

		if choice == "0":
			#Clear screen and exit
			os.system("clear")
			break
		elif choice == "1":
			insert()
		elif choice == "2":
			read()
		elif choice == "3":
			update()
		elif choice == "4":
			delete()
		else:
			print("Invalid option")
			time.sleep(2)

#Start program
menu()

#This section is for test each functions
#menu()
#insert()
#read()
#update()
#delete()
#print(get_all(0, ""))
#print(get_all(1, ""))
#print(get_all(2, ""))
#print(get_all(3, ""))
#print(get_all(4, ""))
#print(get_all(5,("")))