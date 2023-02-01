from flask import Flask, request, jsonify, abort
from models import db
import initial_data
from flask_restful import Api, Resource
import app_functionality


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    api = Api(app)
    api.add_resource(Groups, '/api/v1/groups/')
    api.add_resource(Students, '/api/v1/students/')
    api.add_resource(Courses, '/api/v1/students/<int:student_id>/courses/')
    return app, api


class Groups(Resource):
    def get(self):
        args = request.args
        student_count = args.get('student_count')
        if student_count:
            try:
                return jsonify(app_functionality.find_all_groups(int(student_count)))
            except ValueError:
                return abort(404, description='The student count is invalid')


class Students(Resource):
    def get(self):
        args = request.args
        course_name = args.get('course_name')
        return app_functionality.find_students_by_course(course_name)

    def post(self):
        first_name, last_name = request.form.get('first_name'), request.form.get('last_name')
        if first_name and last_name:
            app_functionality.add_new_student(first_name, last_name)
        else:
            return abort(404, description='First name and the last name are both required')

    def delete(self):
        student_id = request.form.get('student_id')
        if student_id:
            try:
                app_functionality.delete_student(int(student_id))
            except ValueError:
                return abort(404, description='The student ID is invalid')


class Courses(Resource):
    def post(self, student_id):
        given_courses = request.json.get('list_of_courses')
        if isinstance(given_courses, list):
            app_functionality.add_student_to_course(given_courses, student_id)

    def delete(self, student_id):
        given_course = request.json.get('course')
        app_functionality.remove_student_from_course(student_id, given_course)


if __name__ == '__main__':
    app, api = create_app('config.DevelopmentConfig')
    initial_data.create_all_initial_data(app)
    app.run(debug=True)
