"""
Project Name: School Management System
Author: Absera Temesgen
Email: abseratemesgen@gmail.com
Starting Date: January 2021
"""
import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="sclms"
)

db = database.cursor()


class GradeDB:
    @staticmethod
    def getAll():
        """
        Gets all grades from the database without any filter
        """
        statement = """SELECT * FROM grades"""

        db.execute(
            statement
        )
        grades = db.fetchall()
        return grades

    @staticmethod
    def getOne(grade_id):
        """
        gets a single grade by filtering by the grade_id
        """
        statement = """SELECT * FROM grades WHERE grade_id=%s"""
        values = (grade_id,)
        db.execute(
            statement,
            values
        )
        grade = db.fetchall()
        return grade

    @staticmethod
    def add(grade_info):
        """
        accepts a list of fields to add to that grades table
        such as name, description, home room ....
        grade_info might be ["11B", "some description", "Mr. Teacher"]
        """
        statement = """
        INSERT INTO grades (grade_name, grade_description, grade_home_room, grade_class_president, grade_number_of_students, grade_graduation_year) VALUES (%s, %s, %s, %s, %s, %s)
        """
        db.execute(
            statement,
            tuple(grade_info)
        )
        database.commit()

    @staticmethod
    def delete(grade_id):
        statement = """DELETE FROM grades WHERE grade_id=%s"""
        values = (grade_id,)
        db.execute(statement, values)
        database.commit()

    @staticmethod
    def update(updated):
        statement = """UPDATE grades 
        SET grade_name=%s,
        grade_description=%s,
        grade_home_room=%s,
        grade_class_president=%s,
        grade_number_of_students=%s,
        grade_graduation_year=%s
        WHERE grade_id=%s
        """
        values = tuple(updated)
        db.execute(
            statement,
            values
        )
        database.commit()

    @staticmethod
    def doesThisExist(grade_id):
        statement = """SELECT grade_id FROM grades WHERE grade_id=%s"""
        db.execute(statement, (grade_id,))
        grade = db.fetchall()
        if grade:
            return True
        return False


class StudentDB:
    @staticmethod
    def getAll():
        statement = """SELECT * FROM students"""
        db.execute(statement)
        students = db.fetchall()
        return students

    @staticmethod
    def getAllFrom(grade_id, sort_by):
        statement = """SELECT * FROM students WHERE grade_id=%s"""
        values = (grade_id,)
        db.execute(statement, values)
        students = db.fetchall()
        if sort_by == "name-asc":
            students.sort(key=lambda x: x[1])
        elif sort_by == "name-desc":
            students.sort(key=lambda x: x[1], reverse=True)
        return students

    @staticmethod
    def getOne(grade_id, student_id):
        statement = """SELECT * FROM students WHERE grade_id=%s AND student_id=%s"""
        values = (grade_id, student_id,)
        db.execute(statement, values)
        students = db.fetchall()
        return students

    @staticmethod
    def addNew(student_info):
        """
        accepts a list of fields to add to the students table
        such as name, description, home room ....
        grade_info might be ["11B", "some description", "Mr. Teacher"]
        """
        statement = """
        INSERT INTO students (full_name, gender, age, email, parent_phone, student_phone, school_id, locker_key_number, grade_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.execute(
            statement,
            tuple(student_info)
        )
        database.commit()

    @staticmethod
    def search(keyword):
        statement = """SELECT * FROM students WHERE full_name LIKE %s or email LIKE %s or locker_key_number LIKE %s"""
        values = ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%")
        db.execute(statement, values)
        matched_students = db.fetchall()
        return matched_students

    @staticmethod
    def update(updated):
        statement = """UPDATE students 
        SET full_name=%s,
        gender=%s,
        age=%s,
        email=%s,
        parent_phone=%s,
        student_phone=%s,
        school_id=%s,
        locker_key_number=%s
        WHERE grade_id=%s and student_id=%s
        """
        values = tuple(updated)
        db.execute(
            statement,
            values
        )
        database.commit()

    @staticmethod
    def delete(student_id):
        statement = """DELETE FROM students WHERE student_id=%s"""
        values = (student_id,)
        db.execute(statement, values)
        database.commit()

    @staticmethod
    def doesThisExist(student_id):
        statement = """SELECT student_id FROM students WHERE student_id=%s"""
        db.execute(statement, (student_id,))
        student = db.fetchall()
        if student:
            return True
        return False
