import pytest
import psycopg2
from models import db, GroupModel, StudentModel, CourseModel


@pytest.fixture()
def app():
    from main import create_app
    temporal_db_creation()
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
    temporal_db_data_creation(app)
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


def temporal_db_data_creation(app):
    with app.app_context():
        group_names = ['AB-1', 'AB-2', 'AB-3']
        for group_name in group_names:
            new_group = GroupModel(name=group_name)
            db.session.add(new_group)
            db.session.commit()
        course = CourseModel(name='Test Course', description='Test description')
        db.session.add(course)
        student_names = [('Alex', 'Smith', 1), ('Olivia', 'Johnson', 1), ('Alex', 'Williams', 2),
                         ('Emma', 'Brown', 2), ('Oliver', 'Jones', 2), ('James', 'Miller', 3),
                         ('Ava', 'Davis', 3), ('William', 'Garcia', 3), ('Mia', 'Wilson', 3)]
        for student in student_names:
            first_name, last_name, group = student[0], student[1], student[2]
            new_student = StudentModel(first_name=first_name, last_name=last_name)
            new_student.group_id = group
            if first_name == 'Alex':
                new_student.courses.append(course)
            db.session.add(new_student)
            db.session.commit()
