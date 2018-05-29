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
try:
	db_cursor.execute(
		"""
		SELECT articles.title, COUNT(*) as views
		FROM log, articles 
		WHERE '/article/' || articles.slug = path
		GROUP BY title 
		ORDER BY views DESC
		LIMIT 3;
		""")
except:
	print('Query Failed: Could not get the 3 most popular articles')

rows = db_cursor.fetchall()
print('\nResults:\n')
for row in rows:
	print("Article: {} | Popularity: {} total views\n".format(row[0], row[1]))

# Most popular authors
# returns the author's name and the number of views each of their articles has
# gets the author name from the author table by matching up the id in articles with the id in authors
# counts the number of views each article has
db_cursor.execute(
	"""
	SELECT authors.name, COUNT(*) as popularity
	FROM articles, authors, log
	WHERE articles.author = authors.id AND '/article/' || articles.slug = path
	GROUP BY authors.name
	ORDER BY popularity DESC;
	""")

rows = db_cursor.fetchall()
print('\nResults:\n')
for row in rows:
	print("Author: {} | Popularity: {} total views\n".format(row[0], row[1]))

# On which days more than 1% of requests led to errors
# Two subqueries form a table with 200 OK messages and 404 messages
# This could be refactored to just look for the word OK and the word NOT FOUND or other error messages
# After getting the number of both, we can then perform simple arithmatic to get the error percentage
db_cursor.execute(
	"""
	SELECT TRIM(TO_CHAR(status200.day, 'Month')) || TO_CHAR(status200.day, ', DD YYYY'),
	TRUNC(cast(status404.num as decimal) / (status200.num + status404.num), 2) * 100 as error_percentage
	FROM
	(SELECT status, COUNT(*) as num, date(time) as day
	FROM log
	WHERE status = '200 OK'
	GROUP BY status, date(time)) status200,
	(SELECT status, COUNT(*) as num, date(time) as day
	FROM log
	WHERE status = '404 NOT FOUND'
	GROUP BY status, date(time)) status404
	WHERE status200.day = status404.day AND
	cast(status404.num as decimal) / (status200.num + status404.num) > 0.01
	;
	""")

rows = db_cursor.fetchall()
print('\nResults:\n')
for row in rows:
	print("Date: {} | Error Percentage: {}%\n".format(row[0], row[1]))
