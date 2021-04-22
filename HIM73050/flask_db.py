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

__version__ = '0.2p1' #patch Feb 21, 2021
__author__ = 'Stefan V. Pantazi'

from flask import Flask
from flask import g
from . import db_func as dbf

#gdb_conn=None - cannot have the connection object as a global due to the multithreaded nature of flask framework
#gdb_path=None
#gdb_dbname=None
gdb_args={}

_APP_DBREF_ATTR_NAME='_db'

#see https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
#https://docs.python.org/3/library/sqlite3.html

def set_db(aPath,aDbName):
    ''' set the sqlite3 database path and file name'''
    import os.path as path
    if path.exists(aPath):
        global gdb_args
        gdb_args['dbpath']=aPath
        gdb_args['dbname']=aDbName
        print('Set the sqlite3 db engine to path [{0}], database name [{1}]:'.format(aPath,aDbName))
    else:
        raise FileNotFoundError("Error initializing SQLite3 database. Database file path {0} does not exist".format(aPath+aDbName))

def set_db_engine(**dbargs):
    ''' sets the db engine and database connection parameters
        set_db_engine(engine='',host='localhost',user='',password='',dbpath='',dbname='')
        param engine='': default sqlite3
        param dbpath='': location of SQL scripts
    '''

    if not ('engine' in dbargs):#caches the sqlite3 db parameters (path and db file name)
        set_db(dbargs['dbpath'],dbargs['dbname'])
    else:
        #still need to set the dbpath for the access to the SQL scripts
        global gdb_args
        gdb_args=dbargs #caches the argument set - for opening other engine types
        gdb_args.setdefault('host','localhost')
        gdb_args.setdefault('user','')
        gdb_args.setdefault('password','')
        gdb_args.setdefault('dbpath','./')
        gdb_args.setdefault('dbname','')
        #gdb_args.setdefault('engine', 'MYSQL')

        #print('Set the db engine with parameters:',gdb_args)

def get_db():
    ''' gets dbconn from the flask app'''
    db_conn = getattr(g, _APP_DBREF_ATTR_NAME, None)
    if db_conn is None:
        global gdb_args
        db_conn=dbf.db_connection_open_engine(gdb_args)
    return db_conn

def close_db():
    ''' closes flask app db'''
    db_conn = getattr(g, _APP_DBREF_ATTR_NAME, None)
    if db_conn is not None:
        dbf.db_connection_close(db_conn)

def reset_db(schema_script_file,data_clear_script_file,data_load_script_file):
    global gdb_args
    dbConn = dbf.db_connection_open_engine(gdb_args)
    if dbConn:
        if not schema_script_file=="":
            dbf.db_query_script_from_file(dbConn,gdb_args,schema_script_file)
        if not data_clear_script_file=="":
            dbf.db_query_script_from_file(dbConn,gdb_args,data_clear_script_file)
        if not data_load_script_file=="":
            dbf.db_query_script_from_file(dbConn,gdb_args,data_load_script_file)
        dbf.db_connection_close(dbConn)
        return True
    else:
        print('could not reset the database')
        return False

def query_db_get_all(query, args=()):
    cursor=dbf.db_query(get_db(),query,args)
    if cursor:
        results = cursor.fetchall()
        cursor.close()
        return results
    else:
        return None

#TODO: consider adding query_db_get_many()

def query_db_get_one(query, args=()):
    cursor=dbf.db_query(get_db(),query,args)
    if cursor:
        result = cursor.fetchone()
        cursor.close()
        return result
    else:
        return None


def query_db_change(query, args=()):
    db=get_db()
    cursor=dbf.db_query(db,query,args)
    db.commit()
    if cursor:
        lrid=cursor.lastrowid
        cursor.close()
        return lrid
    else:
        return None
def query_db_create(query, args=()):
    cursor=dbf.db_query(get_db(),query,args)
    if cursor:
        cursor.close()
        return True
    else:
        return False


