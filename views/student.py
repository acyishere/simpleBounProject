from asyncio.windows_events import NULL
from types import NoneType
from unittest import result
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
from ..guards import studentGuard

# This file contains views for logged in managers. Each function should be guarded by managerGuard.

@studentGuard
@require_http_methods(["GET"])
def student(req):
    return render(req, 'student.html',{'name': req.session.get('user').get('name')})



@studentGuard
@require_http_methods(["GET"])
def viewCourses(req):
    success = True
    fail = False

    results = []
    try:
        results = run_statement(f"SELECT courses.course_id, courses.name, users.surname, users.department_id, courses.credits, courses.classroom_id, courses.time_slot, courses.quota, GROUP_CONCAT(prerequisite_id) AS prerequisites FROM courses\
            LEFT JOIN prerequisites ON courses.course_id = prerequisites.course_id\
            JOIN users ON users.username = courses.instructor_username\
            GROUP BY courses.course_id")
    except:
        results = []
        fail = True
        success = False

    return render(req, 'instructor/viewCourses.html', {'success': success, 'fail': fail, 'results': results})

@studentGuard
@require_http_methods(["GET"])
def viewTakenCourses(req):
    success = True
    fail = False

    username = req.session.get('user').get('username')
    student_id = req.session.get('user').get('student_id')

    results = []

    try:
        results = run_statement(f"(SELECT student_added_courses.course_id, courses.name, grades.grade FROM student_added_courses \
            JOIN courses ON courses.course_id = student_added_courses.course_id\
            LEFT JOIN grades ON grades.course_id = student_added_courses.course_id and student_added_courses.student_id = grades.student_id\
            WHERE student_added_courses.student_id = {student_id})\
            UNION\
            (SELECT grades.course_id, courses.name, grades.grade FROM grades\
            JOIN courses ON grades.course_id = courses.course_id\
            WHERE grades.student_id = {student_id});")
        results = list(results)
    except:
        results = []
        fail = True
        success = False

    return render(req, 'student/viewTakenCourses.html', {'success': success, 'fail': fail, 'results': results})



@studentGuard
@require_http_methods(["GET"])
def searchCourses(req):
    success = False
    fail = False
    searched_string = req.GET.get('searched_string', False)

    results = []

    if searched_string:
        try:
            success = True
            results = run_statement(f"SELECT courses.course_id, courses.name, users.surname, users.department_id, courses.credits, courses.classroom_id, courses.time_slot, courses.quota, GROUP_CONCAT(prerequisite_id) AS prerequisites FROM courses\
            LEFT JOIN prerequisites ON courses.course_id = prerequisites.course_id\
            JOIN users ON users.username = courses.instructor_username\
            WHERE courses.name LIKE '%{searched_string}%'\
            GROUP BY courses.course_id")
        except:
            results = []
            fail = True
            success = False

    return render(req, 'student/searchCourses.html', {'success': success, 'fail': fail, 'results': results})


@studentGuard
@require_http_methods(["GET"])
def improvedCourseSearch(req):
    success = False
    fail = False
    department_id = req.GET.get('department_ID', False)
    campus = req.GET.get('campus', False)
    min_credits = req.GET.get('min_credits', False)
    max_credits = req.GET.get('max_credits', False)

    results = []

    if department_id and campus and min_credits and max_credits:
        try:
            success = True
            results = run_statement(f"CALL improvedCourseSearch('{department_id}', '{campus}', {min_credits}, {max_credits})")
        except:
            results = []
            fail = True
            success = False

    return render(req, 'student/improvedCourseSearch.html', {'success': success, 'fail': fail, 'results': results})



@studentGuard
@require_http_methods(["GET"])
def addCourse(req):
    success = req.GET.get('success', False)
    fail = req.GET.get('fail', False)

    return render(req, 'student/addCourse.html', {'success': success, 'fail': fail})
