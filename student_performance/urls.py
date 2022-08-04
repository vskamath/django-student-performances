from django import views
from django.urls import path
from student_performance.views import student_performance, hompage, user_logout

urlpatterns = [
    path('', hompage, name='hompage'),                                  # Homepage
    path('view/', student_performance, name='student_performance'),     # Page to view the Student performances
    path('logout/', user_logout, name='user_logout'),                   # Endpoint to logout the student
]