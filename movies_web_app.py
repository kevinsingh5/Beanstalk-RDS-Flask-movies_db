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
    table_ddl = ('CREATE TABLE movies(id INT UNSIGNED NOT NULL AUTO_INCREMENT, '
                    'year INT UNSIGNED NOT NULL, title TEXT NOT NULL, director TEXT, '
                    'actor TEXT, release_date TEXT, rating FLOAT, PRIMARY KEY (id))')

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
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(err.msg)
            

@app.route('/add_movie', methods=['POST'])
def add_movie():
    year = int(request.form['year'])
    title = request.form['title']
    director = request.form['director']
    actor = request.form['actor']
    release_date = request.form['release_date']
    rating = float(request.form['rating'])

    db, username, password, hostname = get_db_creds()
    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password, host=hostname, database=db)
    except Exception as e:
        print(e)

    movie = ("INSERT INTO movies (year, title, director, actor, release_date, rating) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" 
                 % (year, title, director, actor, release_date, rating))
    check = ("SELECT title FROM movies")
    
    message = ('Movie %s successfully inserted' % title)

    cur = cnx.cursor()
    cur.execute(check)
    titles = [dict(title=row[0]) for row in cur.fetchall()]
    for t in titles:
        if t['title'].lower() == title.lower():
            message = ('Movie %s could not be inserted - title already exists' % title)
            return render_template('index.html', message=message)
    
    cur.execute(movie)
    cnx.commit()
    print('Returning from insert_movies()')

    return render_template('index.html', message=message)
    

@app.route('/update_movie', methods=['POST'])
def update_movie():
    year = int(request.form['year'])
    title = request.form['title']
    director = request.form['director']
    actor = request.form['actor']
    release_date = request.form['release_date']
    rating = float(request.form['rating'])

    db, username, password, hostname = get_db_creds()
    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password, host=hostname, database=db)
    except Exception as e:
        print(e)

    movie = ("UPDATE movies SET year='%s', title='%s', director='%s', actor='%s', release_date='%s', rating='%s' WHERE title='%s'"
            % (year, title, director, actor, release_date, rating, title))

    check = ("SELECT title FROM movies")
    cur = cnx.cursor()
    cur.execute(check)
    titles = [dict(title=row[0]) for row in cur.fetchall()]
    for t in titles:
        if t['title'].lower() == title.lower():
            cur.execute(movie)
            message = ('Movie %s successfully updated' % title)
            break
        else:
            message = "Movie %s could not be updated - title doesn't exist" % title

    cnx.commit()
    print('Returning from insert_movies()')
    return render_template('index.html', message=message)


def query_data(): 
    db, username, password, hostname = get_db_creds()

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
    entries = [dict(title=row[0]) for row in cur.fetchall()]
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


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
