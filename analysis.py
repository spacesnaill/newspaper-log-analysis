#!/usr/bin/env python3
import psycopg2
import sys


# check if we can connect to the databse
# if we can connect, say as much
# if we cannot connect, then say so and end the program


# get the db's cursor so we can run queries on the db
# IMPORTANT NOTE: THIS IS A PSYCOPG CURSOR, NOT A POSTGRESQL CURSOR


def db_connect(database_name):
    """
    check if we can connect to the databse
    if we can connect, say as much
    if we cannot connect, then say so and end the program
    get the db's cursor so we can run queries on the db
    IMPORTANT NOTE: THIS IS A PSYCOPG CURSOR, NOT A POSTGRESQL CURSOR
    returns a tuple with the database connection and the cursor
    """
    try:
        db_connection = psycopg2.connect("dbname={}".format(database_name))
        print("Successfully connected to the database")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Not able to connect to database")
        print(error)
        sys.exit(1)

    db_cursor = db_connection.cursor()
    return (db_connection, db_cursor)


db_cursor = db_connect("news")[1]
file_name = 'query_output.txt'
output_file = open(file_name, 'w')


def three_most_popular_articles():
    """
    3 most popular articles
    returns the title of the article and
    looks at the log table to see how many times
    it was accessed, counting those times and also displaying that
    prints the output to the console and to an output file
    """
    query = """
            SELECT articles.title, views
            FROM articles
                INNER JOIN
                (SELECT path, count(path) as views
                FROM log
                GROUP BY log.path) as log
            ON log.path =  '/article/' || articles.slug
            ORDER BY views DESC
            LIMIT 3;
            """
    try:
        db_cursor.execute(query)
        rows = db_cursor.fetchall()

        print('\nThree Most Popular Articles:\n')
        output_file.write('\nThree Most Popular Articles:\n')

        for row in rows:
            output = "Article: {} | Popularity: {} total views\n".format(
                row[0], row[1])
            output_file.write(output)
            print(output)
    except (psycopg2.Error) as e:
        print(e.pgerror)
        output_file.write('Query Failed: ' +
                          'Could not get the 3 most popular articles')
        print('Query Failed: Could not get the 3 most popular articles')


def most_popular_authors():
    """
    Most popular authors
    returns the author's name and
    the number of views each of their articles has
    gets the author name from the author table
    by matching up the id in articles with the id in authors
    counts the number of views each article has
    prints output to console and to output file
    """
    query = """
            SELECT authors.name, COUNT(*) as popularity
            FROM articles, authors, log
            WHERE articles.author = authors.id
            AND '/article/' || articles.slug = path
            GROUP BY authors.name
            ORDER BY popularity DESC;
            """

    try:
        db_cursor.execute(query)
        rows = db_cursor.fetchall()

        print('\nMost Popular Authors:\n')
        output_file.write('\nMost Popular Authors:\n')

        for row in rows:
            output = "Author: {} | Popularity: {} total views\n".format(
                row[0], row[1])
            output_file.write(output)
            print(output)
    except (psycopg2.Error) as e:
        print(e.pgerror)
        output_file.write('Query Failed:' +
                          ' Could not get the most popular authors')
        print('Query Failed: Could not get the most popular authors')


def more_than_one_percent_errors():
    """
    On which days more than 1% of requests led to errors
    Two subqueries form a table with 200 OK messages and 404 messages
    This could be refactored to just look for the word OK
    and the word NOT FOUND or other error messages
    After getting the number of both,
    we can then perform simple arithmatic to get the error percentage
    prints output to console and to output file
    """
    try:
        query = """
            SELECT
            TO_CHAR(status200.day, 'FMMonth DD, YYYY') as long_date,
            ROUND(
            cast(status404.num as decimal) /
            (status200.num + status404.num) * 100, 2)
            as error_percentage
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
            cast(status404.num as decimal) /
            (status200.num + status404.num) > 0.01
            ORDER BY long_date;
            """
        db_cursor.execute(query)
        rows = db_cursor.fetchall()

        output_file.write(
            '\nDays in which more than 1% of Requests led to an error:\n')
        print('\nDays in which more than 1% of Requests led to an error:\n')

        for row in rows:
            output = "Date: {} | Error Percentage: {}%\n".format(
                row[0], row[1])
            output_file.write(output)
            print(output)
    except (psycopg2.Error) as e:
        print(e.pgerror)
        output_file.write(
            'Query Failed: ' +
            'Could not find what days more than 1% of requests led to errors')
        print(
            'Query Failed: ' +
            'Could not find what days more than 1% of requests led to errors')


three_most_popular_articles()
most_popular_authors()
more_than_one_percent_errors()

output_file.close()
