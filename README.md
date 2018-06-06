# Newspaper Analysis

## Description
The point of this program is to run a few queries on the log database of a Newspaper website to gather useful information that can then be interpreted by a user. There are three queries of note here: the 3 most popular newspaper articles, the most popular newspaper authors, and on which days did over 1% of the requests made to the newspaper result in an error.

The Technologies used in this program are as follows:
* [Python 3](https://www.python.org/downloads/)
* [PostgreSQL](https://www.postgresql.org)
* [PsycoPG2](http://initd.org/psycopg/)

Vagrant was also used in this project, but it is not necessarily a requirement for the project to run as long as the news database is already set up on the system in question. With that said, it is **strongly** recommended you use Vagrant. Installation instructions for Vagrant can be found below if the use of Vagrant is desired.

## Setup and Usage
This is the basic setup for the program itself with the use of Vagrant. Installation of Python, PostgreSQL, and PsycoPG2 are all covered in their respective links above if this 

1. Download and Install [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
2. Download and Install [Vagrant](https://www.vagrantup.com/downloads.html), make sure to let it have network permissions if it asks for them
3. Download the [Database SQL file](https://drive.google.com/open?id=1arCNbTJZ44EpWGMJxhUDC_3FZN1xKCsn) and place it in the same directory as the program
4. Open a terminal in the directory of the Vagrant file that came with this program
5. Enter `vagrant up` into the terminal and wait for it to complete
6. Enter `vagrant ssh` into the terminal to ssh into the virtual machine, everything after this point is intended to be performed in the Virtual Machine you just SSH'd into
7. Enter `cd /vagrant` into the terminal to change to the correct directory within the virtual machine where the python file is kept
8. Enter `psql -d news -f newsdata.sql` into the terminal, this will connect to the `news` database and run the SQL commands in the newsdata.sql file
9. Now that everything is setup, run the python file by typing `python analysis.py` into the terminal
10. The output should appear in your terminal window
11. When you wish to stop the virtual machine, simply close the Vagrant SSH terminal window and open a new terminal window in the directory you used `vagrant up` in and enter `vagrant halt` into the terminal