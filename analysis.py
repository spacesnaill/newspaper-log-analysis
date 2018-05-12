import psycopg2
import sys


# check if we can connect to the databse
# if we can connect, good
# if we cannot connect, then say so and end the program
try:
	db = psycopg2.connect("dbname=news")
	print("Successfully connected to the database")
except:
	print("Not able to connect to database")
	sys.exit(1)

