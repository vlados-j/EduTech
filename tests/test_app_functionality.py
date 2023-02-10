from models import db, GroupModel, CourseModel, StudentModel
from app_functionality import find_all_groups, find_students_by_course, add_new_student, delete_student, \
    add_student_to_course, remove_student_from_course


def test_find_all_groups(app):
    with app.app_context():
        assert find_all_groups(3) == ['AB-1', 'AB-2']


def test_find_students_by_course(app):
    with app.app_context():
        assert find_students_by_course('Blockchain Technology') == ['Alex Smith', 'Alex Williams']


def test_add_new_student(app):
    with app.app_context():
        add_new_student(first_name='TestUser', last_name='TestUser')
        student = db.session.execute(db.select(StudentModel).where(StudentModel.first_name == 'TestUser')).scalars().first()
        assert student.id == 10
        assert student.first_name == 'TestUser'
        assert student.last_name == 'TestUser'


def test_delete_student(app):
    with app.app_context():
        delete_student(1)
        student_from_db = db.session.execute(db.select(StudentModel).where(StudentModel.id == 1)).scalars().first()
        assert student_from_db is None


def test_add_student_to_course(app):
    with app.app_context():
        add_student_to_course(['Blockchain Technology', 'Fake Course'], 2)
        student = db.session.execute(db.select(StudentModel).where(StudentModel.id == 2)).scalars().first()
        course = [course.name for course in student.courses]
        assert course == ['Blockchain Technology']


def test_remove_student_from_course(app):
    with app.app_context():
        remove_student_from_course(1, 'Blockchain Technology')
        student = db.session.execute(db.select(StudentModel).where(StudentModel.id == 1)).scalars().first()
        assert student.courses == []
