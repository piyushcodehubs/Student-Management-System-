from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path("students/",views.student_list, name="student_list"),
    path("students/add",views.add_student,name="add_student"),
    path('Services/',views.services,name="services"),
    path("about/",views.about, name="about"),
    path("Contact/",views.contact,name="contact"),
    path("students/<int:student_id>",views.delete_student, name="delete_student"),
    path(
    "students/edit/<int:student_id>/",
    views.edit_student,
    name="edit_student"),

]

