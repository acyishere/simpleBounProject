from asyncio.windows_events import NULL
from sre_constants import SUCCESS
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
from ..guards import managerGuard

# This file contains views for logged in managers. Each function should be guarded by managerGuard.

@managerGuard
@require_http_methods(["GET"])
def manager(req):
    return render(req, 'manager.html',{'username': req.session.get('user').get('username')})

#Add a new user
@managerGuard
@require_http_methods(["GET"])
def addNewUser(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)
    return render(req, 'manager/addNewUser.html', {'success': success, 'fail': fail})

#Delete a student
@managerGuard
@require_http_methods(["GET"])
def deleteStudent(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)
    return render(req, 'manager/deleteStudent.html', {'success': success, 'fail': fail})

#Update Instructor Title
@managerGuard
@require_http_methods(["GET"])
def updateInstructorTitle(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)
    return render(req, 'manager/updateInstructorTitle.html', {'success': success, 'fail': fail})

#View Students
@managerGuard
@require_http_methods(["GET"])
def viewStudents(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)

    students = run_statement(f"SELECT users.username, users.name, users.surname, users.email, users.department_id,\
        students.completed_Credits, students.GPA FROM Students\
        JOIN Users ON Students.username = Users.username ORDER BY completed_Credits ASC;")

    return render(req, 'manager/viewStudents.html', {'success': success, 'fail': fail, 'students': students})

#View Instructors
@managerGuard
@require_http_methods(["GET"])
def viewInstructors(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)

    instructors = run_statement(f"SELECT users.username, users.name, users.surname, users.email, users.department_id,\
    instructors.title FROM Instructors \
    JOIN Users ON Instructors.username = Users.username;")

    return render(req, 'manager/viewInstructors.html', {'success': success, 'fail': fail, 'instructors': instructors})


@managerGuard
@require_http_methods(["GET"])
def viewInstructors(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)

    instructors = run_statement(f"SELECT users.username, users.name, users.surname, users.email, users.department_id,\
    instructors.title FROM Instructors \
    JOIN Users ON Instructors.username = Users.username;")

    return render(req, 'manager/viewInstructors.html', {'success': success, 'fail': fail, 'instructors': instructors})


@managerGuard
@require_http_methods(["GET"])
def viewGrades(req):
    success = False
    fail = False
    student_id = req.GET.get('student_id', False)

    grades = []
    if student_id:
        success = True
        try:
            grades = run_statement(f"SELECT courses.course_id, courses.name, grades.grade FROM grades\
                JOIN courses ON courses.course_id = grades.course_id\
                WHERE grades.student_id={student_id};")
        except:
            grades = []
            fail = True
            success = False

    return render(req, 'manager/viewGrades.html', {'success': success, 'fail': fail, 'grades': grades})


@managerGuard
@require_http_methods(["GET"])
def viewInstructorCourses(req):
    success = False
    fail = False
    username = req.GET.get('username', False)

    courses = []
    if username:
        success = True
        try:
            courses = run_statement(f"SELECT courses.course_id, courses.name, courses.classroom_id, classrooms.campus, courses.time_slot FROM courses\
                JOIN classrooms ON courses.classroom_id = classrooms.classroom_id\
                WHERE courses.instructor_username = '{username}';")
        except:
            courses = []
            fail = True
            success = False

    return render(req, 'manager/viewInstructorCourses.html', {'success': success, 'fail': fail, 'results': courses})



@managerGuard
@require_http_methods(["GET"])
def viewGradeAverage(req):
    success = False
    fail = False
    course_id = req.GET.get('course_id', False)

    results = []
    if course_id:
        success = True
        try:
            results = run_statement(f"SELECT grades.course_id, courses.name, sum(grades.grade) / count(grades.grade) AS grade_average FROM grades\
                JOIN courses ON courses.course_id = grades.course_id\
                WHERE grades.course_id = '{course_id}'\
                GROUP BY grades.course_id;")
        except:
            results = []
            fail = True
            success = False

    return render(req, 'manager/viewGradeAverage.html', {'success': success, 'fail': fail, 'results': results})


