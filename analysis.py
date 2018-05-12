import psycopg2
import sys


# check if we can connect to the databse
# if we can connect, say as much
# if we cannot connect, then say so and end the program
try:
	db_connection = psycopg2.connect("dbname=news")
	print("Successfully connected to the database")
except:
	print("Not able to connect to database")
	sys.exit(1)

# get the db's cursor so we can run queries on the db
# IMPORTANT NOTE: THIS IS A PSYCOPG CURSOR, NOT A POSTGRESQL CURSOR
db_cursor = db_connection.cursor()

# using the cursor, queries can be found below

db_cursor.execute(
	"""articles.title, count(*) as num 
	from log, articles 
	where replace(lower(title),' ', '-') 
	like 
	ltrim(path, '/article/') 
	group by title 
	order by num desc; """)


