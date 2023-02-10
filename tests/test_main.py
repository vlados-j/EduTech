from models import db, StudentModel, CourseModel, GroupModel


def test_Groups_get_positive(client, app):
    with app.app_context():
        group_names = ['AB-1', 'AB-2', 'AB-3']
        for group_name in group_names:
            new_group = GroupModel(name=group_name)
            db.session.add(new_group)
            db.session.commit()
        student_names = [('Alex', 'Smith', 'AB-1'), ('Olivia', 'Johnson', 'AB-1'), ('Noah', 'Williams', 'AB-2'),
                         ('Emma', 'Brown', 'AB-2'), ('Oliver', 'Jones', 'AB-2'), ('James', 'Miller', 'AB-3'),
                         ('Ava', 'Davis', 'AB-3'), ('William', 'Garcia', 'AB-3'), ('Mia', 'Wilson', 'AB-3')]
        for student in student_names:
            first_name, last_name, group = student[0], student[1], student[2]
            new_student = StudentModel(first_name=first_name, last_name=last_name)
            new_student.group_id = group
            db.session.add(new_student)
            db.session.commit()
    response = client.get('/api/v1/groups/?student_count=3')
    assert response.data == b'[\n  "AB-1",\n  "AB-2"\n]\n'
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_Groups_get_negative(client, app):
    response = client.get('/api/v1/groups/?student_count=surprise')
    assert response.status_code == 404


def test_Students_get(client, app):
    with app.app_context():
        course = CourseModel(name='Blockchain Technology', description='Test description')
        db.session.add(course)
        students = [('Alex', 'Smith'), ('Olivia', 'Johnson')]
        for first_name, last_name in students:
            student = StudentModel(first_name=first_name, last_name=last_name)
            student.courses.append(course)
            db.session.add(student)
        db.session.commit()
    response = client.get('/api/v1/students/?course_name=Blockchain+Technology')
    assert response.data == b'[\n    "Alex Smith",\n    "Olivia Johnson"\n]\n'
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_Students_post_positive(client, app):
    response = client.post('/api/v1/students/', data={
        'first_name': 'Alex',
        'last_name': 'Smith'
    })
    assert response.status_code == 200


def test_Students_post_negative(client, app):
    response = client.post('/api/v1/students/', data={
        'first_name': 'Alex'
    })
    assert response.status_code == 404


def test_Students_delete_positive(client, app):
    with app.app_context():
        student = StudentModel(first_name='Alex', last_name='Smith')
        db.session.add(student)
        db.session.commit()
    response = client.delete('/api/v1/students/', data={
        'student_id': '1'
    })
    assert response.status_code == 200


def test_Students_delete_negative(client):
    response = client.delete('/api/v1/students/', data={
        'student_id': 'fail'
    })
    assert response.status_code == 404


def test_Courses_post(client):
    response = client.post('/api/v1/students/1/courses/', json={
        'list_of_courses': '["Blockchain Technology", "Fake Course"]'
    })
    assert response.status_code == 200


def test_Course_delete(client):
    response = client.delete('/api/v1/students/1/courses/', json={
        'course': 'Blockchain Technology'
    })
    assert response.status_code == 200
