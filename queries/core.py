from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
import hashlib


@require_http_methods(["POST"])
def loginAsStudent(req):
    username = req.POST["username"]
    password = req.POST["password"]

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    result=run_statement(f"SELECT users.username, users.name, users.surname, users.email, users.department_id, students.student_id FROM users\
        JOIN students ON users.username = students.username\
        WHERE users.username='{username}' AND users.password='{hashed_password}' AND  users.is_student") #Run the query in DB
    
    if result:
        user_tuple = result[0]
        user = {
            'username': user_tuple[0],
            'name': user_tuple[1],
            'surname': user_tuple[2],
            'email': user_tuple[3],
            'role': 'student',
            'department_id': user_tuple[4],
            'student_id': user_tuple[5]
        }
        req.session['user'] = user
        return HttpResponseRedirect("/simpleboun/student/")
    else:
        return HttpResponseRedirect("/simpleboun/studentLogin?fail=true")
    

@require_http_methods(["POST"])
def loginAsInstructor(req):
    username = req.POST["username"]
    password = req.POST["password"]

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    result=run_statement(f"SELECT * FROM users WHERE username='{username}' AND password='{hashed_password}' AND NOT is_student;") #Run the query in DB
    
    if result:
        user_tuple = result[0]
        user = {
            'username': user_tuple[0],
            'name': user_tuple[1],
            'surname': user_tuple[2],
            'email': user_tuple[4],
            'role': 'instructor',
            'department_id': user_tuple[5],
        }
        req.session['user'] = user
        return HttpResponseRedirect("/simpleboun/instructor/")
    else:
        return HttpResponseRedirect("/simpleboun/instructorLogin?fail=true")



@require_http_methods(["POST"])
def loginAsManager(req):
    username = req.POST["username"]
    password = req.POST["password"]

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    result=run_statement(f"SELECT * FROM managers WHERE username='{username}' AND password='{hashed_password}';") #Run the query in DB
    
    print(hashed_password)

    if result:
        user_tuple = result[0]
        user = {
            'username': user_tuple[0],
            'role': 'manager'
        }
        req.session['user'] = user
        return HttpResponseRedirect("/simpleboun/manager/")
    else:
        return HttpResponseRedirect("/simpleboun/managerLogin?fail=true")
    

@require_http_methods(["POST"])
def logout(req):
    req.session.flush()
    return HttpResponseRedirect("/simpleboun")




