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

# 3 most popular articles
# returns the title of the article and looks at the log table to see how many times
# it was accessed, counting those times and also displaying that
db_cursor.execute(
	"""
	SELECT articles.title, COUNT(*) as views
	FROM log, articles 
	WHERE articles.slug = LTRIM(path, '/article/')
	GROUP BY title 
	ORDER BY views DESC;
	""")

# Most popular authors
db_cursor.execute(
	"""
	SELECT authors.name, COUNT(*) as popularity
	FROM articles, authors, log
	WHERE articles.author = authors.id AND articles.slug LIKE LTRIM(path, '/article/')
	GROUP BY authors.name
	ORDER BY popularity DESC;
	""")

