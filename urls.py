from django.urls import path

from . import views
from . import queries

#This file connects functions with html files.

urlpatterns = [
    path('', views.views.index, name='index'),
    path('studentLogin/', views.authentication.studentLogin, name='studentLogin'), 
    path('instructorLogin/', views.authentication.instructorLogin, name='instructorLogin'),
    path('managerLogin/', views.authentication.managerLogin, name='managerLogin'),
    path('student/', views.student.student, name='student'),
    path('manager/', views.manager.manager, name='manager'),
    path('instructor/', views.instructor.instructor, name='student'),
    path('manager/addNewUser/', views.manager.addNewUser, name='managerAddNewUser'),
    path('manager/deleteStudent/', views.manager.deleteStudent, name='managerDeleteUser'),
    path('manager/viewStudents/', views.manager.viewStudents, name='managerViewStudents'),
    path('manager/viewInstructors/', views.manager.viewInstructors, name='managerViewInstructors'),
    path('manager/viewInstructorCourses/', views.manager.viewInstructorCourses, name='managerViewInstructorCourses'),
    path('manager/updateInstructorTitle/', views.manager.updateInstructorTitle, name='managerUpdateInstructorTitle'),
    path('manager/viewGrades/', views.manager.viewGrades, name='studentViewGrades'),
    path('manager/addNewUser/query/', queries.manager.addNewUser, name='addNewUserQuery'),
    path('manager/deleteStudent/query/', queries.manager.deleteStudent, name='deleteStudentQuery'),
    path('manager/updateInstructorTitle/query/', queries.manager.updateInstructorTitle, name='updateInstructorTitleQuery'),
    path('instructor/viewCourseStudents/', views.instructor.viewCourseStudents, name='instructorViewCourseStudents'),
    path('manager/viewGradeAverage/', views.manager.viewGradeAverage, name='managerViewGradeAverage'),
    path('instructor/listClassrooms/', views.instructor.listClassrooms, name='instructorListClassrooms'),
    path('instructor/addCourse/', views.instructor.addCourse, name='instructorAddCourse'),
    path('instructor/updateCourseName/', views.instructor.updateCourseName, name='instructorUpdateCourseName'),
    path('student/viewTakenCourses/', views.student.viewTakenCourses, name='studentViewTakenCourses'),
    path('instructor/updateCourseName/query/', queries.instructor.updateCourseName, name='instructorUpdateCourseNameQuery'),
    path('instructor/addCourse/query/', queries.instructor.addCourse, name='instructorAddCourse'),
    path('instructor/addPrerequisite/', views.instructor.addPrerequisite, name='instructorAddPrerequisite'),
    path('instructor/addPrerequisite/query/', queries.instructor.addPrerequisite, name='instructorAddPrerequisiteQuery'),
    path('instructor/viewCourses/', views.instructor.viewCourses, name='instructorViewCourses'),
    path('instructor/giveGrade/', views.instructor.giveGrade, name='instructorGiveGrade'),
    path('instructor/giveGrade/query/', queries.instructor.giveGrade, name='instructorGiveGradeQuery'),
    path('student/viewCourses/', views.student.viewCourses, name='studentViewCourses'),
    path('student/searchCourses/', views.student.searchCourses, name='studentSearchCourses'),
    path('student/improvedCourseSearch/', views.student.improvedCourseSearch, name='studentImprovedCourseSearch'),
    path('student/addCourse/', views.student.addCourse, name='studentAddCourse'),
    path('student/addCourse/query/', queries.student.addCourse, name='studentAddCourseQuery'),
    path('loginAsStudent/', queries.core.loginAsStudent, name='loginAsStudent'),
    path('loginAsInstructor/', queries.core.loginAsInstructor, name='loginAsInstructor'),
    path('loginAsManager/', queries.core.loginAsManager, name='loginAsManager'),
    path('logout/', queries.core.logout, name='logout'),
]