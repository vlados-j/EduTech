import main
from models import db, CourseModel, StudentModel, GroupModel, students_courses


def find_all_groups(student_count: int):
    """Find all groups with less or equals student count."""
    with main.app.app_context():
        all_courses = db.session.execute(db.select(GroupModel.name).
                                         join(StudentModel, StudentModel.group_id == GroupModel.name).
                                         group_by(GroupModel.name).
                                         having(db.func.count(StudentModel.id) <= student_count))
        return all_courses.scalars().all()


def find_students_by_course(course_name: str):
    """Find all students related to the course with a given name."""
    with main.app.app_context():
        students = db.session.execute(db.select(StudentModel).join(students_courses).
                                      where(students_courses.columns.course_name == course_name)).scalars().all()
        return [f'{student.first_name} {student.last_name}' for student in students]


def add_new_student(first_name: str, last_name: str):
    """Add new student"""
    with main.app.app_context():
        new_student = StudentModel(first_name=first_name, last_name=last_name)
        db.session.add(new_student)
        db.session.commit()


def delete_student(student_id: int):
    """Delete student by STUDENT_ID"""
    with main.app.app_context():
        student = db.session.execute(db.select(StudentModel).where(StudentModel.id == student_id)).scalars().first()
        if student:
            db.session.delete(student)
            db.session.commit()


def add_student_to_course(list_of_courses: list, student_id: int):
    """Add a student to the course (from a list)"""
    with main.app.app_context():
        student = db.session.execute(db.select(StudentModel).where(StudentModel.id == student_id)).scalars().first()
        if student:
            all_courses = db.session.execute(db.select(CourseModel).
                                             where(CourseModel.name.in_(list_of_courses))).scalars().all()
            for given_course in all_courses:
                student.courses.append(given_course)
                db.session.commit()


def remove_student_from_course(student_id: int, course: str):
    """Remove the student from one of his or her courses"""
    with main.app.app_context():
        student = db.session.execute(db.select(StudentModel).where(StudentModel.id == student_id)).scalars().first()
        if student:
            course = db.session.execute(db.select(CourseModel).where(CourseModel.name == course)).scalars().first()
            if course in student.courses:
                student.courses.remove(course)
                db.session.commit()

