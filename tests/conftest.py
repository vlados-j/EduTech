import pytest
import psycopg2
from models import db


@pytest.fixture()
def app():
    from main import create_app
    temporal_db_creation()
    app, api = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.engine.dispose()
    temporal_db_deletion()


@pytest.fixture()
def client(app):
    return app.test_client()


def temporal_db_creation():
    conn = psycopg2.connect(
       database="postgres", user='postgres', password='qwerty', host='127.0.0.1', port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql_command = '''CREATE database test_university'''
    cursor.execute(sql_command)
    conn.close()


def temporal_db_deletion():
    conn = psycopg2.connect(
       database="postgres", user='postgres', password='qwerty', host='127.0.0.1', port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql_command3 = '''DROP DATABASE test_university;'''
    cursor.execute(sql_command3)
    conn.close()
