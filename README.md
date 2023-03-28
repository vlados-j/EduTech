# EduTech

Edutech is the application that inserts/select/updates/deletes data in the database <b>PostgreSQL using SQLAlchemy and Flask REST Framework</b>.

In this application I was practicing the skills in CRUD operations using PostgreSQL, SQLAlchemy and Flask REST Framework. 

The app generates 10 groups with randomly generated names, 10 courses (math, biology, etc), 200 students. After that, randomly assigns students to groups, and courses. 

The APIs were designed using the best practises described by Brian Mulloy in a book "Web API DesignCrafting Interfaces that Developers Love". 

Using different endpoints we can find all groups with less or equals student count, find all students related to the course with a given name, add new student, delete student by STUDENT_ID, add a student to the course (from a list), remove the student from one of his or her courses.

APIs and other functionality tested using pytest. 
