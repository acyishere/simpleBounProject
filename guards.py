from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .db_utils import run_statement
from django.views.decorators.http import require_http_methods


def studentGuard(func):
    def inner(req):
        if not req.session.get('user'):
            return HttpResponseRedirect("/simpleboun/studentLogin")

        role = req.session.get('user').get('role')
        if role == 'student':
            return func(req)
        elif role == 'instructor': 
            return HttpResponseRedirect("/simpleboun/instructor/")
        elif role == 'manager':
            return HttpResponseRedirect("/simpleboun/manager/")
        else:
            req.session.flush()
            return HttpResponseRedirect("/simpleboun")
    return inner

def instructorGuard(func):
    def inner(req):
        if not req.session.get('user'):
            return HttpResponseRedirect("/simpleboun/instructorLogin")

        role = req.session.get('user').get('role')
        if role == 'student':
            return HttpResponseRedirect("/simpleboun/student/")
        elif role == 'instructor': 
            return func(req)
        elif role == 'manager':
            return HttpResponseRedirect("/simpleboun/manager/")
        else:
            req.session.flush()
            return HttpResponseRedirect("/simpleboun")
    return inner


def managerGuard(func):
    def inner(req):
        if not req.session.get('user'):
            return HttpResponseRedirect("/simpleboun/managerLogin")

        role = req.session.get('user').get('role')
        if role == 'student':
            return HttpResponseRedirect("/simpleboun/student/")
        elif role == 'instructor': 
            return HttpResponseRedirect("/simpleboun/instructor/")
        elif role == 'manager':
            return func(req)
        else:
            req.session.flush()
            return HttpResponseRedirect("/simpleboun")
    return inner


def guestGuard(func):
    def inner(req):
        if not req.session.get('user'):
            return func(req)

        role = req.session.get('user').get('role')
        if role == 'student':
            return HttpResponseRedirect("/simpleboun/student/")
        elif role == 'instructor': 
            return HttpResponseRedirect("/simpleboun/instructor/")
        elif role == 'manager':
            return HttpResponseRedirect("/simpleboun/manager/")
        else:
            req.session.flush()
            return HttpResponseRedirect("/simpleboun")
    return inner