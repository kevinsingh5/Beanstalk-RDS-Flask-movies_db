import os
import time

from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode

movies_web_app = Flask(__name__)
app = movies_web_app


def get_db_creds():
    db = os.environ.get("RDS_DB_NAME", None) or os.environ.get("DB", None)
    username = os.environ.get("RDS_USERNAME", None) or os.environ.get("USER", None)
    password = os.environ.get("RDS_PASSWORD", None) or os.environ.get("PASSWORD", None)
    hostname = os.environ.get("RDS_HOSTNAME", None) or os.environ.get("HOST", None)
    return db, username, password, hostname


def create_table():
    # Check if table exists or not. Create and populate it only if it does not exist.
    db, username, password, hostname = get_db_creds()
    table_ddl = 'CREATE TABLE movies(id INT UNSIGNED NOT NULL AUTO_INCREMENT, year TEXT, title TEXT, director TEXT, actor TEXT, release_date TEXT, rating TEXT, PRIMARY KEY (id))'

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    try:
        cur.execute(table_ddl)
        cnx.commit()
        #add_movie()
        #populate_data()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(err.msg)
            

@app.route('/add_movie', methods=['POST'])
def add_movie():
    app.logger.error('INSIDE insert_movie()')

    year = request.form['year']
    title = request.form['title']
    director = request.form['director']
    actor = request.form['actor']
    release_date = request.form['release_date']
    rating = request.form['rating']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password, host=hostname, database=db)
    except Exception as e:
        print(e)

    #movie = "INSERT INTO movies (year, title, director, actor, release_date, rating) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (year, title, director, actor, release_date, rating)
    movie = "INSERT INTO movies(year, title, director, actor, release_date, rating) VALUES ('2020', 'hardcoded', 'kevin', 'ratnika', 'july', '5')" 


    cur = cnx.cursor()
    cur.execute(movie)
    app.logger.error('PAST EXECUTE INSERT COMMAND %s' % title)
    cnx.commit()
    print('Returning from insert_movies()')
    message = 'Movie successfully inserted'

    return render_template('index.html', message=message)
    

'''
def populate_data():

    db, username, password, hostname = get_db_creds()

    print("Inside populate_data")
    print("DB: %s" % db)
    print("Username: %s" % username)
    print("Password: %s" % password)
    print("Hostname: %s" % hostname)

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                       host=hostname,
                                       database=db)
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    cur.execute("INSERT INTO message (greeting) values ('Hello, World!')")
    cnx.commit()
    print("Returning from populate_data")
    '''


def query_data(): 
    db, username, password, hostname = get_db_creds()

    app.logger.error("INSIDE query_data")
    print("DB: %s" % db)
    print("Username: %s" % username)
    print("Password: %s" % password)
    print("Hostname: %s" % hostname)

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()

    cur.execute("SELECT title FROM movies")
    entries = [dict(title=row[2]) for row in cur.fetchall()]
    app.logger.error('BEFORE RETURNING ENTRIES')
    return entries

try:
    print("---------" + time.strftime('%a %H:%M:%S'))
    print("Before create_table")
    create_table()
    app.logger.error("After create_table")
except Exception as exp:
    print("Got exception %s" % exp)
    conn = None

'''
@app.route('/add_to_db', methods=['POST'])
def add_to_db():
    print("Received request.")
    print(request.form['message'])
    msg = request.form['message']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)
        #import MySQLdb
        #cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db)

    cur = cnx.cursor()
    cur.execute("INSERT INTO message (greeting) values ('" + msg + "')")
    cnx.commit()
    return hello()
    '''


@app.route("/")
def hello():
#    print("Printing available environment variables")
 #   print(os.environ)
  #  print("Before displaying index.html")
    #entries = query_data()
    #print("Entries: %s" % entries)
    return render_template('index.html')#, entries=entries)

# @app.route("/")
def checkout():
    print("Inside checkout")
    print("Printing available environment variables")
    print(os.environ)
    print("Before displaying checkout.html")
    entries = query_data()
#    message = add_movie()
    print("Entries: %s" % entries)
    return render_template('index.html', entries=entries)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
