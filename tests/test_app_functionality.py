from models import db, GroupModel, CourseModel, StudentModel
from app_functionality import find_all_groups, find_students_by_course, add_new_student, delete_student, \
    add_student_to_course, remove_student_from_course


def test_find_all_groups(app):
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
        assert find_all_groups(3) == ['AB-1', 'AB-2']


def test_find_students_by_course(app):
    with app.app_context():
        course = CourseModel(name='Blockchain Technology', description='Test description')
        db.session.add(course)
        students = [('Alex', 'Smith'), ('Olivia', 'Johnson')]
        for first_name, last_name in students:
            student = StudentModel(first_name=first_name, last_name=last_name)
            student.courses.append(course)
            db.session.add(student)
        db.session.commit()
        assert find_students_by_course('Blockchain Technology') == ['Alex Smith', 'Olivia Johnson']


def test_add_new_student(app):
    with app.app_context():
        add_new_student(first_name='Alex', last_name='Smith')
        student = db.session.execute(db.select(StudentModel)).scalars().first()
        assert student.id == 1
        assert student.first_name == 'Alex'
        assert student.last_name == 'Smith'


def test_delete_student(app):
    with app.app_context():
        student = StudentModel(first_name='Alex', last_name='Smith')
        db.session.add(student)
        db.session.commit()
        delete_student(1)
        student_from_db = db.session.execute(db.select(StudentModel).where(StudentModel.id == 1)).scalars().first()
        assert student_from_db is None


def test_add_student_to_course(app):
    with app.app_context():
        student = StudentModel(first_name='Alex', last_name='Smith')
        db.session.add(student)
        course = CourseModel(name='Blockchain Technology')
        db.session.add(course)
        db.session.commit()
        add_student_to_course(['Blockchain Technology', 'Fake Course'], 1)
        course = [course.name for course in student.courses]
        assert course == ['Blockchain Technology']


def test_remove_student_from_course(app):
    with app.app_context():
        student = StudentModel(first_name='Alex', last_name='Smith')
        db.session.add(student)
        course = CourseModel(name='Blockchain Technology')
        db.session.add(course)
        student.courses.append(course)
        db.session.commit()
        remove_student_from_course(1, 'Blockchain Technology')
        assert student.courses == []
