from models import db, StudentModel, GroupModel, CourseModel
# from sqlalchemy import *
# from flask_sqlalchemy import SQLAlchemy
# import psycopg2


def test_request_example(client):
    response = client.get('/api/v1/groups/?student_count=40')
    print(response.data) #['XF-81', 'OC-69', 'AY-14', 'LK-22', 'HQ-07', 'DO-41', 'VE-47', 'RE-42', 'QY-32', 'EP-96']
    assert response.status_code == 200

