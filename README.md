# pyCRUD
Basic CRUD with Python
=============================
Developed by: Gilberto Delgado<br>
https://github.com/hilliyo/pyCRUD<br>
Version: 1.0 (Linux)<br>
Python Version: 3<br>
Date: Aug. 30th, 2022<br>

README:
This is a command-line-based program that inserts, modified, reads and deletes information from a table in a database with MySQL.

How to use?

1. Run script "db.sql" to create the database that works with this program.
   Do this with the following command:

		mysql -u root -p < db.sql

   Enter password and wait that process ends.

   WARNING! If you have a database with name "movies" this action will delete it.

2. Run file "crud.py" with the following command:
   
		python3 crud.py

3. Enjoy!