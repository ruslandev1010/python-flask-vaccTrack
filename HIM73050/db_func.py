'''
    Copyright (C) 2021 Stefan V. Pantazi (svpantazi@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.
'''

__version__ = '0.2p1'
__author__ = 'Stefan V. Pantazi'

import sqlite3
from sqlite3 import Error
'''
  based on: https://docs.python.org/3/library/sqlite3.html
'''

def db_connection_open(db_file):
    ''' SQLite3 connection open - needs a db file only'''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #no need for commit for data modifying queries; data changes (for INSERT,REPLACE,UPDATE,DELETE type queries) are immediate in this isolation level
        conn.isolation_level="IMMEDIATE"
        def build_dictionary(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        #conn.row_factory=sqlite3.Row
        conn.row_factory=build_dictionary

        print("database {0} opened".format(db_file))
    except Error as e:
        print("DB connection opening error: ",e)
    return conn

def db_connection_open_mysql(dbargs):
    conn = None
    try:
        import pymysql
        import pymysql.cursors
        conn=pymysql.connect(
                        host=dbargs['host'],
                        user=dbargs['user'],
                        password=dbargs['password'],
                        db=dbargs['dbname'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
        print("mysql database {0} opened".format(dbargs['dbname']))
    except pymysql.OperationalError as e:
        print("DB connection opening error: ",e)
    return conn

def db_connection_open_mariadb(dbargs):
    '''untested'''
    conn = None
    try:
        import mariadb
        conn=mariadb.connect(
                        host=dbargs['host'],
                        user=dbargs['user'],
                        password=dbargs['password'],
                        database=dbargs['dbname'])
        print("mariadb database {0} opened".format(dbargs['dbname']))
    except mariadb.OperationalError as e:
        print("DB connection opening error: ",e)
    return conn

def db_connection_open_engine(dbargs):
    if not 'engine' in dbargs or dbargs['engine'].lower().find('sqlite')>=0 : #default is SQLITE, all it needs is gdb path and file
        conn = db_connection_open(dbargs['dbpath']+dbargs['dbname'])
    elif dbargs['engine']=='MYSQL':
        conn = db_connection_open_mysql(dbargs)
    elif dbargs['engine']=='MARIADB':
        conn = db_connection_open_mariadb(dbargs)
    else:
        raise Exception("Error opening the database engine {0}.".format(dbargs['engine']))
    return conn

def db_connection_close(conn):
    try:
        conn.close()
        print("database closed")
    except Error as e:
        print("DB connection closing error: ",e)
    return conn

def db_query(conn, sql_query_string,args=()):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query_string,args)
        return cursor
    except Error as e:
        print("DB query error:",e)


def parse_sql(sqlString):
    lines=sqlString.split(';')
    sqlScript = []
    for l in lines:
        l=l.strip('\n')
        l=l.replace('\n',' ')
        if len(l)>0:
            sqlScript.append(l+';')
    return sqlScript

    return stmts

def db_query_script(conn, dbargs, sql_query_script):
    try:
        cursor = conn.cursor()
        if not 'engine' in dbargs or dbargs['engine'].lower().find('sqlite')>=0 : #default is SQLITE, all it needs is gdb path and file:
            cursor.executescript(sql_query_script)
        elif dbargs['engine']=='MYSQL':
            #must separate SQL query lines and execute each one; bummer :()
            #cursor.execute(sql_query_script)
            sql_lines = parse_sql(sql_query_script)
            for line in sql_lines:
                cursor.execute(line)
            #conn.commit()
        return cursor
    except Error as e:
        print("DB query error:",e)

def db_query_script_from_file(conn,dbargs, sql_script_file):
    with open(dbargs['dbpath']+sql_script_file,"r") as file:
        try:
            SQL_script_string=file.read()
            return db_query_script(conn,dbargs,SQL_script_string)
        except Error as e:
            print("DB query error:",e)
        finally:
            file.close()


