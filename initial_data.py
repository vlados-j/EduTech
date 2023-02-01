from models import db, StudentModel, GroupModel, CourseModel
from sqlalchemy.exc import ProgrammingError
import random
import string


def create_all_initial_data(app):
    try:
        with app.app_context():
            db.session.execute(db.select(StudentModel))
    except ProgrammingError:
        create_tables(app)
        create_groups(app)
        create_courses(app)
        create_students(app)
        assign_students_to_groups(app)
        many_to_many_creation(app)


def create_tables(app):
    with app.app_context():
        db.create_all()


def create_groups(app):
    with app.app_context():
        for i in range(0, 10):
            group = GroupModel(name=group_name_generator())
            db.session.add(group)
            db.session.commit()


def group_name_generator():
    uppercase_letters = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
    digits = random.choice(string.digits) + random.choice(string.digits)
    return uppercase_letters + '-' + digits


def create_courses(app):
    subjects = [('Artificial Intelligences', 'Such programs cover various programming languages, tools, and libraries '
                                             'to equip students with the required competencies.'),
                ('Blockchain Technology', 'Blockchain is a rapidly growing discipline capable of bringing about signif'
                                          'icant transformations in the fields of real estate, healthcare, finance, in'
                                          'surance, among several others.'),
                ('Business Analytics', 'The Business Analytics Certification is one of the trending courses 2023 has '
                                       'drawn attention to, especially for those competing for business analyst and ma'
                                       'nagerial roles. '),
                ('Data Science', 'Study programs in data science typically focus on big data analytics, data visualiza'
                                 'tion, statistics, and predictive analytics.'),
                ('Digital Marketing', 'Digital marketing is an exciting subject for professionals like brand managers,'
                                      ' sales personnel, entrepreneurs, and marketers.'),
                ('Management', 'Their insights can translate into actionable metrics, leading to changes in planning, '
                               'operations, product development, and strategic management.'),
                ('Product Management', 'Project managers ensure that work assignments are delivered within time and b'
                                       'udget constraints.'),
                ('Big Data', 'Big data certifications can help you go after more diverse roles than specific data sc'
                             'ience jobs.'),
                ('Cloud Computing', 'Cloud computing is one of the top IT fields that is experiencing an emerging tren'
                                    'd in 2023.'),
                ('Cybersecurity', 'In the wake of rising cyber crimes, the demand for security experts has also picked'
                                  ' up.')]
    with app.app_context():
        for subject, description in subjects:
            course = CourseModel(name=subject, description=description)
            db.session.add(course)
            db.session.commit()


def create_students(app):
    with app.app_context():
        for name in random_names():
            first_name, last_name = name.split()
            student = StudentModel(first_name=first_name, last_name=last_name)
            db.session.add(student)
            db.session.commit()


def random_names():
    result = []
    names = ['Liam', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Charlotte', 'Elijah', 'Amelia', 'James', 'Ava', 'William',
             'Sophia', 'Benjamin', 'Isabella', 'Lucas', 'Mia', 'Henry', 'Evelyn', 'Theodore', 'Harper']
    surnames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson',
                'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson', 'Thompson',
                'White']
    while len(result) != 200:
        random_name = random.choice(names) + ' ' + random.choice(surnames)
        if random_name not in result:
            result.append(random_name)
    return result


def assign_students_to_groups(app):
    with app.app_context():
        all_students = db.session.execute(db.select(StudentModel))
        groups = db.session.execute(db.select(GroupModel))
        list_of_groups = [group.name for group in groups.scalars().all()]
        list_of_groups.append(None)
        for student in all_students.scalars().all():
            student.group_id = random.choice(list_of_groups)
            db.session.commit()


def many_to_many_creation(app):
    with app.app_context():
        all_students = db.session.execute(db.select(StudentModel)).scalars().all()
        all_courses = db.session.execute(db.select(CourseModel)).scalars().all()
        for student in all_students:
            for i in range(1, random.randint(2, 4)):
                while True:
                    course = random.choice(all_courses)
                    if course not in student.courses:
                        student.courses.append(course)
                        db.session.commit()
                        break
