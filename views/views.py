from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ..db_utils import run_statement
from django.views.decorators.http import require_http_methods
from ..guards import studentGuard, instructorGuard, managerGuard, guestGuard

# Create your views here.

# user = {
#     'username': '',
#     'name': '',
#     'surname': '',
#     'role': '',
#     'department_id': '',
#     'email': ''
# }

class User:
    def __init__(self,username, name, surname, email, role, department_id):
        self.username = username
        self.name = name
        self.surname = surname
        self.role = role
        self.department_id = department_id
        self.email = email
    
@guestGuard
@require_http_methods(["GET"])
def index(req):
    if not req.session.get('user'):
        return render(req, 'landingPage.html',{})

    role = req.session.get('user').get('role')
    if role == 'student':
        return HttpResponseRedirect("/simpleboun/student/")
    elif role == 'instructor': 
        pass
    elif role == 'manager':
        pass
    else:
        req.session.flush()
        return HttpResponseRedirect("/simpleboun")

@studentGuard
@require_http_methods(["GET"])
def student(req):
    return render(req, 'student.html',{})


