"""
Project Name: School Management System
Author: Absera Temesgen
Email: abseratemesgen@gmail.com
Starting Date: January 2021
Updated here
"""

from flask import Flask, render_template, redirect, request, url_for
from db import GradeDB, StudentDB
from model import GradeFromRaw, StudentsFromRaw

app = Flask(__name__)
app.secret_key = "ntawxerjwt"


##################################################
##################################################

@app.route("/")
@app.route("/grades", methods=["GET"])
def viewGrades():
    rawGrades = GradeDB.getAll()
    grades = GradeFromRaw().init(rawGrades).grades
    return render_template("grade/grades.html", grades=grades)


@app.route("/grades/<int:grade_id>")
def viewSingleGrade(grade_id):
    # sorting methods
    sort_by = request.args.get("sort_by", "name-asc")

    grade = students = None
    if GradeDB.doesThisExist(grade_id):
        rawGrades = GradeDB.getOne(grade_id)
        rawStudents = StudentDB.getAllFrom(grade_id, sort_by=sort_by)

        grade = GradeFromRaw().init(rawGrades).grades[0]
        students = StudentsFromRaw().init(rawStudents).students
    return render_template("grade/single_grade.html",
                           grade=grade, students=students)


@app.route("/grades/add", methods=["GET", "POST"])
def addNewGrade():
    if request.method == "GET":
        pass
    if request.method == "POST":
        gn = request.form.get("grade-name")
        desc = request.form.get("description")
        hr = request.form.get("home-room")
        pres = request.form.get("president")
        n = request.form.get("n-of-students")
        gy = request.form.get("graduation-year")

        packed_info = [gn, desc, hr, pres, n, gy]
        GradeDB.add(packed_info)
        return redirect("/grades")
    return render_template("grade/add_grade.html")


@app.route("/grades/<int:grade_id>/update", methods=["GET", "POST"])
def updateGrade(grade_id):
    grade = None
    if GradeDB.doesThisExist(grade_id):
        rawGrades = GradeDB.getOne(grade_id)
        grade = GradeFromRaw().init(rawGrades).grades[0]
        if request.method == "POST":
                gn = request.form.get("grade-name")
                desc = request.form.get("description")
                hr = request.form.get("home-room")
                pres = request.form.get("president")
                n = request.form.get("n-of-students")
                gy = request.form.get("graduation-year")

                packed_info = [gn, desc, hr, pres, n, gy, grade_id]
                GradeDB.update(updated=packed_info)
    return render_template("grade/update_grade.html", grade=grade)


@app.route("/grades/<int:grade_id>/delete", methods=["GET", "POST"])
def deleteGrade(grade_id):
    if GradeDB.doesThisExist(grade_id):
        GradeDB.delete(grade_id)
    return redirect("/grades")


##################################################
##################################################


@app.route("/students", methods=["GET", "POST"])
def viewAllStudents():
    rawStudent = StudentDB.getAll()
    students = StudentsFromRaw().init(rawStudent).students
    if request.method == "POST":
        search_text = request.form.get("search-input")
        raw_search_match = StudentDB.search(search_text)
        students = StudentsFromRaw().init(raw_search_match).students
    return render_template("student/students.html", students=students)


@app.route("/grades/<int:grade_id>/students/<int:student_id>",
           methods=["GET"])
def viewSingleStudent(grade_id, student_id):
    student = None
    if StudentDB.doesThisExist(student_id) and GradeDB.doesThisExist(grade_id):
        rawStudents = StudentDB.getOne(grade_id, student_id)
        student = StudentsFromRaw.init(rawStudents).students[0]
    else:
        # todo error page here too
        return redirect("/error")
    return render_template("student/single_student.html",
                           student=student)


@app.route("/grades/<int:grade_id>/students/add", methods=["GET", "POST"])
def addNewStudent(grade_id):
    # add new student in a particular grade
    if request.method == "POST":
        if GradeDB.doesThisExist(grade_id):
            full_name = request.form.get("full-name")
            gender = request.form.get("gender")
            age = request.form.get("age")
            email = request.form.get("email")
            parent_phone = request.form.get("parent-phone")
            student_phone = request.form.get("student-phone")
            school_id = request.form.get("school-id")
            loker = request.form.get("locker-key-number")

            student_info = [full_name, gender, age, email, parent_phone, student_phone, school_id, loker, grade_id]
            if full_name and gender and age:
                StudentDB.addNew(student_info)
                return redirect(f"/grades/{grade_id}")
            else:
                pass
                # todo show some alert to enter all values
        else:
            # todo redirect to does not exist page
            return redirect("/error")
    return render_template("student/add_student.html", grade_id=grade_id)


@app.route("/grades/<int:grade_id>/students/<int:student_id>/update",
           methods=["GET", "POST"])
def updateStudent(grade_id, student_id):
    # update student in a particular grade
    rawStudentInfo = StudentDB.getOne(grade_id, student_id)
    student = StudentsFromRaw().init(rawStudentInfo).students[0]
    if request.method == "POST":
        if StudentDB.doesThisExist(student_id) and GradeDB.doesThisExist(grade_id):
            full_name = request.form.get("full-name")
            gender = request.form.get("gender")
            age = request.form.get("age")
            email = request.form.get("email")
            parent_phone = request.form.get("parent-phone")
            student_phone = request.form.get("student-phone")
            school_id = request.form.get("school-id")
            loker = request.form.get("locker-key-number")

            updatedStudent = [full_name, gender, age, email, parent_phone, student_phone, school_id, loker, grade_id,
                              student_id]
            StudentDB.update(updatedStudent)
            return redirect(f"/grades/{grade_id}")
        else:
            # todo redirect to error page
            return redirect("/error")
    return render_template("student/update_student.html", student=student)

@app.route("/students/<int:student_id>/delete/")
def deleteStudentFromStudents(student_id):
    """
    This one deletes a student from students page and redirects to students page
    """
    if StudentDB.doesThisExist(student_id):
        StudentDB.delete(student_id)
    else:
        return redirect("/students")

@app.route("/grades/<int:grade_id>/students/<int:student_id>/delete",
           methods=["GET", "POST"])
def deleteStudentFromGrades(grade_id, student_id):
    """
    This one deletes a student from grades page and redirects to grades page after deleting
    """
    if GradeDB.doesThisExist(grade_id) and StudentDB.doesThisExist(student_id):
        StudentDB.delete(student_id)
        return redirect(f"/grades/{grade_id}")
    else:
        return redirect("/grades")


##################################################
##################################################

if __name__ == "__main__":
    app.run(debug=True)
