from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
from ..guards import instructorGuard

# This file contains views for logged in managers. Each function should be guarded by managerGuard.

@instructorGuard
@require_http_methods(["GET"])
def instructor(req):
    return render(req, 'instructor.html',{'name': req.session.get('user').get('name')})


@instructorGuard
@require_http_methods(["GET"])
def listClassrooms(req):
    success = False
    fail = False
    time_slot = req.GET.get('time_slot', False)

    results = []
    if time_slot:
        success = True
        try:
            results = run_statement(f"SELECT classroom_id, campus, capacity FROM classrooms\
                WHERE not EXISTS (\
                    SELECT * FROM courses WHERE courses.classroom_id = classrooms.classroom_id AND courses.time_slot = {time_slot}\
                );")
        except:
            results = []
            fail = True
            success = False

    return render(req, 'instructor/listClassrooms.html', {'success': success, 'fail': fail, 'results': results})


@instructorGuard
@require_http_methods(["GET"])
def addCourse(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)
    return render(req, 'instructor/addCourse.html', {'success': success, 'fail': fail})

@instructorGuard
@require_http_methods(["GET"])
def addPrerequisite(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)
    return render(req, 'instructor/addPrerequisite.html', {'success': success, 'fail': fail})


@instructorGuard
@require_http_methods(["GET"])
def viewCourses(req):
    success = True
    fail = False

    username = req.session.get('user').get('username')

    results = []
    try:
        results = run_statement(f"SELECT courses.course_id, name, classroom_id, time_slot, quota, GROUP_CONCAT(prerequisite_id) AS prerequisites FROM courses\
            LEFT JOIN prerequisites ON courses.course_id = prerequisites.course_id\
            WHERE instructor_username = '{username}'\
            GROUP BY courses.course_id")
    except:
        results = []
        fail = True
        success = False

    return render(req, 'instructor/viewCourses.html', {'success': success, 'fail': fail, 'results': results})


@instructorGuard
@require_http_methods(["GET"])
def giveGrade(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)
    return render(req, 'instructor/giveGrade.html', {'success': success, 'fail': fail})

    
@instructorGuard
@require_http_methods(["GET"])
def updateCourseName(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)
    return render(req, 'instructor/updateCourseName.html', {'success': success, 'fail': fail})

@instructorGuard
@require_http_methods(["GET"])
def viewCourseStudents(req):
    success = False
    fail = False
    course_id = req.GET.get('course_id', False)
    username = req.session.get('user').get('username')

    results = []

    if course_id:

        try:

            check1 = run_statement(f"SELECT * FROM courses WHERE course_id = '{course_id}' AND instructor_username = '{username}';")
            if len(check1) == 0:
                raise Exception("Course doesn't belong to authenticated instructor.")

            results = run_statement(f"SELECT users.username, students.student_id, users.email, users.name , users.surname FROM users \
            JOIN students ON students.username = users.username \
            JOIN student_added_courses ON student_added_courses.student_id = students.student_id \
            WHERE student_added_courses.course_id = '{course_id}';")
            success = True
        except:
            results = []
            fail = True
            success = False

    return render(req, 'instructor/viewCourseStudents.html', {'success': success, 'fail': fail, 'results': results})
