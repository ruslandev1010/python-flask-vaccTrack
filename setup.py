#needs this to fix the fact that modINFO74000 module is not in the same directory
import os
import sys
from flask import Flask

app = Flask(__name__)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../libs')))
print('Sys path: ',sys.path)

_APP_NAME='VaccTrack'

#database
_MEASUREMENTS_TABLE='Measurements'
_PATIENTS_TABLE='Patients'

_DB_ENGINE='MYSQL'#'MYSQL'

_PORT=5000
_HOST='127.0.0.1'

_RESET_DB=False

from HIM73050.flask_db import set_db,reset_db, set_db_engine

if _DB_ENGINE=='MYSQL':
    _PLACEHOLDER='%s'
    set_db_engine(
            engine='MYSQL',
            host='localhost',
            user='root',
            password='',
            dbpath=os.path.join(os.path.dirname(__file__),'database/mariadb/'),
            dbname='vacc_track')
else:
    _PLACEHOLDER='?'
    #set_db(os.path.join(os.path.dirname(__file__),'database/sqlite3/'),'bpappdb.sqlite')
    set_db_engine(engine='sqlite3',dbpath=os.path.join(os.path.dirname(__file__),'database/sqlite3/'),dbname='bpappdb.sqlite')


if _RESET_DB:
    if reset_db('schema.sql','clean-data.sql','insert-data.sql'):
        print("database was reset")

