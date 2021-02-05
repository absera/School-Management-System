"""
Project Name: School Management System
Author: Absera Temesgen
Email: abseratemesgen@gmail.com
Starting Date: January 2021
"""
class Grade:
    """
    A grade model that accepts grade_id and name
    and makes it simple to access the two fields.
    It's used in GradeFromRaw.init()
    """

    def __init__(self,
                 grade_id,
                 name,
                 description,
                 home_room,
                 class_president,
                 number_of_students,
                 graduation_year):
        self.grade_id = grade_id
        self.name = name
        self.description = description
        self.home_room = home_room
        self.class_president = class_president
        self.number_of_students = number_of_students
        self.graduation_year = graduation_year


class Grades:
    """
    This is a class to store a list of Grade objects.
    It's used in GradeFromRaw.init()
    """

    def __init__(self):
        self.grades = []

    def add(self, grade):
        self.grades.append(grade)

    def get(self):
        return self.grades


class GradeFromRaw:
    def __init__(self):
        pass

    @staticmethod
    def init(rawList):
        grade_list = Grades()
        for rawGrade in rawList:
            grade_list.add(Grade(
                grade_id=rawGrade[0],
                name=rawGrade[1],
                description=rawGrade[2],
                home_room=rawGrade[3],
                class_president=rawGrade[4],
                number_of_students=rawGrade[5],
                graduation_year=rawGrade[6]
            ))
        return grade_list


class Student:
    """
    A student is a model to get access to name, gender and stuff of a student
    """

    def __init__(self,
                 id_,
                 name,
                 gender,
                 age,
                 grade_,
                 email,
                 parent_phone,
                 student_phone,
                 school_id,
                 locker_key_number,
                 ):
        self.id = id_
        self.name = name
        self.gender = gender
        self.age = age
        self.grade = grade_
        self.email = email
        self.parent_phone = parent_phone
        self.phone_number = student_phone
        self.school_id = school_id
        self.locker_key_number = locker_key_number


class Students:
    def __init__(self):
        self.students = []

    def add(self, student_):
        self.students.append(student_)

    def get(self):
        return self.students


class StudentsFromRaw:
    @staticmethod
    def init(rawStudents):
        student_list = Students()
        for rawStudent in rawStudents:
            student_list.add(Student(
                id_=rawStudent[0],
                name=rawStudent[1],
                gender=rawStudent[2],
                age=rawStudent[3],
                grade_=rawStudent[4],
                email=rawStudent[5],
                parent_phone=rawStudent[6],
                student_phone=rawStudent[7],
                school_id=rawStudent[8],
                locker_key_number=rawStudent[9],
            ))
        return student_list


###############################################
###############################################

