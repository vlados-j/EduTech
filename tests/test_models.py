from models import db, StudentModel, GroupModel, CourseModel


def test_GroupModel(app):
    with app.app_context():
        group = GroupModel(name='AB-12')
        db.session.add(group)
        db.session.commit()
        group_from_db = db.session.execute(db.select(GroupModel)).scalars().first()
        assert group_from_db.name == 'AB-12'


def test_StudentModel(app):
    with app.app_context():
        group = GroupModel(name='AB-12')
        db.session.add(group)
        student = StudentModel(first_name='Alex', last_name='Miller')
        student.group_id = 'AB-12'
        db.session.add(student)
        db.session.commit()
        student_from_db = db.session.execute(db.select(StudentModel)).scalars().first()
        print(student_from_db.id, student_from_db.first_name, student_from_db.last_name, student_from_db.group_id)
        assert student_from_db.id == 1
        assert student_from_db.first_name == 'Alex'
        assert student_from_db.last_name == 'Miller'
        assert student_from_db.group_id == 'AB-12'


def test_CourseModel(app):
    with app.app_context():
        course = CourseModel(name='Blockchain Technology', description='Test Description')
        db.session.add(course)
        db.session.commit()
        course_from_db = db.session.execute(db.select(CourseModel)).scalars().first()
        assert course_from_db.name == 'Blockchain Technology'
        assert course_from_db.description == 'Test Description'
