# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, random, string

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    #SERVER_NAME = 'servicos.educorp.unicamp.br'
    #PREFERRED_URL_SCHEME = 'https'

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/frequencia/static/assets')  
    URL_ADDCLASS = os.getenv('URL_ADDCLASS', 'https://servicos.educorp.unicamp.br/frequencia/add_class')
    URL_LOGOUT = os.getenv('URL_LOGOUT', 'https://servicos.educorp.unicamp.br/frequencia/logout')
    URL_INDEX = os.getenv('URL_INDEX', 'https://servicos.educorp.unicamp.br/frequencia/index')
    URL_ATTEND = os.getenv('URL_ATTEND', 'https://servicos.educorp.unicamp.br/frequencia/attend')
    URL_ATTEND_DATA = os.getenv('URL_ATTEND_DATA', '/frequencia/attendance_data')
    URL_ATTEND_DATA_CSV = os.getenv('URL_ATTEND_DATA_CSV', 'https://servicos.educorp.unicamp.br/frequencia/export_attendance_csv')
    URL_ATTEND_DATA_CSV_ALL = os.getenv('URL_ATTEND_DATA_CSV_ALL', 'https://servicos.educorp.unicamp.br/frequencia/export_attendance_csv_all')
    URL_ARCHIVE = os.getenv('URL_ARCHIVE', 'https://servicos.educorp.unicamp.br/frequencia/archive_class')
    URL_ARCHIVED_CLASSES = os.getenv('URL_ARCHIVED_CLASSES', 'https://servicos.educorp.unicamp.br/frequencia/archived_classes')
    URL_DELETE = os.getenv('URL_DELETE', 'https://servicos.educorp.unicamp.br/frequencia/delete_class')
    URL_FREQUENCIA = os.getenv('URL_FREQUENCIA', 'https://servicos.educorp.unicamp.br/frequencia/attendance_data2')

    # Set up the App SECRET_KEY
    SECRET_KEY  = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))     

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    USE_SQLITE  = True 

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USERNAME:

        try:
            
            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE,
                DB_USERNAME,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME
            ) 

            USE_SQLITE  = False

        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )
            print('> Fallback to SQLite ')    

    if USE_SQLITE:

        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    
class ProductionConfig(Config):
    DEBUG = False
    #SERVER_NAME = 'servicos.educorp.unicamp.br'
    #PREFERRED_URL_SCHEME = 'https'
    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
