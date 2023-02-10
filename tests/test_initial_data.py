from initial_data import create_groups, group_name_generator, create_courses, create_students, random_names, \
    assign_students_to_groups, many_to_many_creation
from models import db, GroupModel, CourseModel, StudentModel
from unittest.mock import patch


def test_create_groups(app):
    create_groups(app)
    with app.app_context():
        group = db.session.execute(db.select(GroupModel)).scalars().first()
        assert isinstance(group, GroupModel)


def test_group_name_generator():
    group_name = group_name_generator()
    assert group_name[2] == '-'
    assert group_name[3:].isdigit()
    assert group_name[0:2].isalpha()
    assert group_name[0:2].isupper()


def test_create_courses(app):
    create_courses(app)
    with app.app_context():
        course = db.session.execute(db.select(CourseModel).
                                    where(CourseModel.name == 'Blockchain Technology')).scalars().first()
        assert course.description == 'Blockchain is a rapidly growing discipline capable of bringing about significant' \
                                     ' transformations in the fields of real estate, healthcare, finance, insurance, ' \
                                     'among several others.'


def test_create_students(app):
    create_students(app)
    with app.app_context():
        random_student = db.session.execute(db.select(StudentModel)).scalars().first()
        assert isinstance(random_student, StudentModel)


def test_random_names():
    names = random_names()
    random_name = names[0]
    assert len(names) == 200
    assert len(random_name.split()) == 2


@patch('initial_data.random.choice')
def test_assign_students_to_groups(mocked_random, app):
    mocked_random.return_value = 'AB-12'
    with app.app_context():
        group = GroupModel(name='AB-12')
        db.session.add(group)
        student = StudentModel(first_name='Alex', last_name='Miller')
        db.session.add(student)
        db.session.commit()
        assign_students_to_groups(app)
        student_from_db = db.session.execute(db.select(StudentModel)).scalars().first()
        assert student_from_db.group_id == 'AB-12'


@patch('initial_data.random.randint')
def test_many_to_many_creation(mocked_randint, app):
    mocked_randint.return_value = 2
    with app.app_context():
        course = CourseModel(name='Blockchain Development', description='Test Description')
        db.session.add(course)
        student = StudentModel(first_name='Alex', last_name='Miller')
        db.session.add(student)
        db.session.commit()
        many_to_many_creation(app)
        student_from_db = db.session.execute(db.select(StudentModel)).scalars().first()
        assert isinstance(student_from_db.courses[0], CourseModel)
