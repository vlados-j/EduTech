from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


students_courses = db.Table('students_courses',
                            db.Column('id', db.Integer, primary_key=True),
                            db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                            db.Column('course_name', db.String, db.ForeignKey('courses.name')))


class GroupModel(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    students = db.relationship('StudentModel', backref='groups')


class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    courses = db.relationship('CourseModel', secondary=students_courses, backref='students')


class CourseModel(db.Model):
    __tablename__ = "courses"
    name = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
