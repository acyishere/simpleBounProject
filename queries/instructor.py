from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
from ..guards import instructorGuard

#Instructor adds new Course to system.
@instructorGuard
@require_http_methods(["POST"])
def addCourse(req):
    course_id = req.POST["course_id"]
    name = req.POST["name"]
    credits = req.POST["credits"]
    classroom_id = req.POST["classroom_id"]
    time_slot = req.POST["time_slot"]
    quota = req.POST["quota"]
    instructor_username = req.session.get('user').get('username')
    capacity = run_statement(f"SELECT capacity FROM classrooms \
    WHERE classroom_id = '{classroom_id}';")

    try:
        if int(capacity[0][0]) >= int(quota):
            try:
                run_statement(f"INSERT INTO courses VALUES('{course_id}','{name}',{credits},{quota},'{instructor_username}','{classroom_id}',{time_slot});")
                return HttpResponseRedirect("/simpleboun/instructor/addCourse?success=true")
            except:
                return HttpResponseRedirect("/simpleboun/instructor/addCourse?fail=true")
    
        else:
            return HttpResponseRedirect("/simpleboun/instructor/addCourse?fail=true")
    
    except:
        return HttpResponseRedirect("/simpleboun/instructor/addCourse?fail=true")


@instructorGuard
@require_http_methods(["POST"])
def addPrerequisite(req):
    course_id = req.POST["course_id"]
    prerequisite_course_id = req.POST["prerequisite_course_id"]

    try:
        run_statement(f"INSERT INTO prerequisites VALUES('{course_id}','{prerequisite_course_id}');")
        return HttpResponseRedirect("/simpleboun/instructor/addPrerequisite?success=true")
    except:
        return HttpResponseRedirect("/simpleboun/instructor/addPrerequisite?fail=true")


@instructorGuard
@require_http_methods(["POST"])
def giveGrade(req):
    course_id = req.POST["course_id"]
    student_id = req.POST["student_id"]
    grade = req.POST["grade"]

    username = req.session.get('user').get('username')

    try:
        check1 = run_statement(f"SELECT * FROM courses WHERE course_id = '{course_id}' AND instructor_username = '{username}';")
        if len(check1) == 0:
            raise Exception("Course doesn't belong to authenticated instructor.")
        check2 = run_statement(f"SELECT * FROM student_added_courses WHERE student_id = {student_id} AND course_id = '{course_id}';")
        if len(check2) == 0:
            raise Exception("Student has not added course.")
        run_statement(f"INSERT INTO grades VALUES('{student_id}','{course_id}',{grade});")
        return HttpResponseRedirect("/simpleboun/instructor/giveGrade?success=true")
    except:
        return HttpResponseRedirect("/simpleboun/instructor/giveGrade?fail=true")


@instructorGuard
@require_http_methods(["POST"])
def updateCourseName(req):
    course_id = req.POST["course_id"]
    name = req.POST["name"]

    username = req.session.get('user').get('username')

    allCourses = run_statement(f"SELECT course_id FROM courses WHERE instructor_username='{username}';")

    if (course_id,) in allCourses: #burda yukarda yeni yazcagım query den dönen list verilen course id yi contain ediyo mu diye control etcem.
        try:
            run_statement(f"UPDATE courses SET name = '{name}' WHERE course_id ='{course_id}';")
            return HttpResponseRedirect("/simpleboun/instructor/updateCourseName?success=true")
        except:
            return HttpResponseRedirect("/simpleboun/instructor/updateCourseName?fail=true")
    else:
        return HttpResponseRedirect("/simpleboun/instructor/updateCourseName?fail=true")
