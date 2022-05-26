from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
from ..guards import managerGuard
import hashlib

# This file contains views for logged in managers. Each function should be guarded by managerGuard.

#Manager adds new user to system.
@managerGuard
@require_http_methods(["POST"])
def addNewUser(req):
    username = req.POST["username"]
    name = req.POST["name"]
    surname = req.POST["surname"]
    password = req.POST["password"]
    email = req.POST["e-mail"]
    type = req.POST.get('type', None)
    is_student = "True" if type == "Student" else "False"
    department_id = req.POST["department_id"]
    student_id = req.POST["student_id"]
    title = req.POST.get("title")

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        run_statement(f"INSERT INTO users VALUES('{username}','{name}','{surname}','{hashed_password}','{email}',{is_student}, '{department_id}');")

        if type == "Student":
            run_statement(f"INSERT INTO students VALUES('{student_id}', '{username}', 0.0, 0);")
        else:
            run_statement(f"INSERT INTO instructors VALUES('{username}', '{title}');")
        return HttpResponseRedirect("/simpleboun/manager/addNewUser?success=true")
    except Exception as e:
        print(e)
        return HttpResponseRedirect("/simpleboun/manager/addNewUser?fail=true")

#Manager deletes students by providing student_id.
@managerGuard
@require_http_methods(["POST"])
def deleteStudent(req):
    student_id = req.POST["student_id"]

    try:
        run_statement(f"DELETE FROM students WHERE student_id={student_id};")
        return HttpResponseRedirect("/simpleboun/manager/deleteStudent?success=true")
    except:
        return HttpResponseRedirect("/simpleboun/manager/deleteStudent?fail=true")

#Manager updates instructor titles by providing username and new title.
@managerGuard
@require_http_methods(["POST"])
def updateInstructorTitle(req):

    username = req.POST["username"]
    title = req.POST.get('title', "")

    print(title)

    try:
        run_statement(f"UPDATE instructors SET title = '{title}' WHERE username ='{username}';")
        return HttpResponseRedirect("/simpleboun/manager/updateInstructorTitle?success=true")
    except:
        return HttpResponseRedirect("/simpleboun/manager/updateInstructorTitle?fail=true")
  
        

