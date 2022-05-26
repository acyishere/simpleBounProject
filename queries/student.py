from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
from ..guards import studentGuard

@studentGuard
@require_http_methods(["POST"])
def addCourse(req):
    course_id = req.POST["course_id"]
    
    student_id = req.session.get('user').get('student_id')
    print(req.session.get('user'))

    try:
        # Student can not take the course twice. (check if there is a grade for the course)
        check1 = run_statement(f"SELECT * FROM grades\
            WHERE student_id = {student_id} AND course_id = '{course_id}'")
        if len(check1) > 0:
            raise Exception("Student can not take the course twice.")
        
        # For each prerequisite of course, check if there exists a record in grades.
        check2 = run_statement(f"SELECT * FROM prerequisites\
            WHERE course_id = '{course_id}' AND NOT EXISTS (\
                SELECT * FROM grades\
                WHERE grades.course_id = prerequisites.prerequisite_id AND grades.student_id = {student_id}\
            )")
        if len(check2) > 0:
            raise Exception("Student should have taken the prerequisite courses before taking the course.")

        # Check if course quota is full
        check3 = run_statement(f"SELECT quota - student_count FROM\
            (SELECT quota FROM courses\
            WHERE course_id = '{course_id}') AS q,\
            (SELECT count(*) AS student_count FROM student_added_courses\
            WHERE course_id = '{course_id}') AS s")
        if check3[0][0] <= 0:
            raise Exception("Course quota is full.")

        # Constraints hold so add the course.
        run_statement(f"INSERT INTO student_added_courses VALUES('{course_id}', {student_id});")
        return HttpResponseRedirect("/simpleboun/student/addCourse?success=true")
    except:
        return HttpResponseRedirect("/simpleboun/student/addCourse?fail=true")
