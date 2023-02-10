

def test_groups_get_positive(client):
    response = client.get('/api/v1/groups/?student_count=3')
    assert response.json == ['AB-1', 'AB-2']
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_groups_get_negative(client):
    response = client.get('/api/v1/groups/?student_count=surprise')
    assert response.status_code == 404


def test_students_get(client):
    response = client.get('/api/v1/students/?course_name=Test+Course')
    assert response.json == ['Alex Smith', 'Alex Williams']
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_students_post_positive(client):
    response = client.post('/api/v1/students/', data={
        'first_name': 'TestUser',
        'last_name': 'TestUser'
    })
    assert response.status_code == 200


def test_students_post_negative(client):
    response = client.post('/api/v1/students/', data={
        'first_name': 'TestUser'
    })
    assert response.status_code == 404


def test_students_delete_positive(client):
    response = client.delete('/api/v1/students/', data={
        'student_id': '1'
    })
    assert response.status_code == 200


def test_students_delete_negative(client):
    response = client.delete('/api/v1/students/', data={
        'student_id': 'fail'
    })
    assert response.status_code == 404


def test_courses_post(client):
    response = client.post('/api/v1/students/1/courses/', json={
        'list_of_courses': '["Test Course", "Fake Course"]'
    })
    assert response.status_code == 200


def test_course_delete(client):
    response = client.delete('/api/v1/students/1/courses/', json={
        'course': 'Test Course'
    })
    assert response.status_code == 200
