# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
# Import dotenv to load environment variables
from dotenv import load_dotenv

# Assuming your .env file is in the same directory as this script, or specify the path explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    @app.context_processor
    def inject_globals():
        return {
            'ASSETS_ROOT': app.config.get('ASSETS_ROOT', '/static/assets'),
            'URL_ADDCLASS': app.config.get('URL_ADDCLASS'),
            'URL_LOGOUT': app.config.get('URL_LOGOUT'),
            'URL_INDEX': app.config.get('URL_INDEX'),
            'URL_ATTEND': app.config.get('URL_ATTEND'),
            'URL_ATTEND_DATA': app.config.get('URL_ATTEND_DATA'),
            'URL_ATTEND_DATA_CSV': app.config.get('URL_ATTEND_DATA_CSV'),
            'URL_ATTEND_DATA_CSV_ALL': app.config.get('URL_ATTEND_DATA_CSV_ALL'),
            'URL_ARCHIVE': app.config.get('URL_ARCHIVE'),
            'URL_ARCHIVED_CLASSES': app.config.get('URL_ARCHIVED_CLASSES'),
            'URL_DELETE': app.config.get('URL_DELETE'),
            'URL_FREQUENCIA': app.config.get('URL_FREQUENCIA'),
        }
    
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
