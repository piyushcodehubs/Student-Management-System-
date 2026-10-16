from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Student
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count

# Create your views here.
# def home(request):
#   # return HttpResponse("hello")
#   return render(request,"students/home.html")

def home(request):
    total_students = Student.objects.count()

    total_courses = Student.objects.values(
        "course"
    ).distinct().count()

    recent_students = Student.objects.order_by(
        "-enrollment_date"
    )[:5]

    context = {
        "total_students": total_students,
        "total_courses": total_courses,
        "recent_students": recent_students,
    }

    return render(request, "students/home.html", context)

def services(request):
  return render(request, "students/Services.html")

def about(request):
  return render(request, "students/About.html")

def contact(request):
  return render(request, "students/Contact.html")



def student_list(request):
    query = request.GET.get("q", "").strip()

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )

    return render(request, "students/student_list.html", {
        "students": students
    })



def add_student(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        course = request.POST.get("course", "").strip()

        if not all([full_name, email, phone, course]):
            return render(request, "students/add_student.html", {
                "error": "All fields are required."
            })
        if Student.objects.filter(email=email).exists():
            return render(request, "students/add_student.html", {
                "error": "This email is already registered."
            })

        Student.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            course=course
        )
        messages.success(request, "Student added successfully!")

        return redirect("student_list")

    return render(request, "students/add_student.html")



def delete_student(request, student_id):
    if request.method == "POST":
        student = Student.objects.get(id=student_id)
        student.delete()
        messages.success(request, "Student deleted successfully!")
    return redirect("student_list")



def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        course = request.POST.get("course", "").strip()

        if not all([full_name, email, phone, course]):
          messages.error(request, "All fields are required.")
          return render(
              request,
              "students/edit_student.html",
              {"student": student}
          )

        # if Student.objects.filter(email=email).exclude(id=student.id).exists():
        #     messages.error(request, "This email belongs to another student.")
        #     return render(
        #         request,
        #         "students/edit_student.html",
        #         {"student": student}
        #     )
        if Student.objects.filter(email=email).exclude(id=student.id).exists():
          messages.error(request, "This email belongs to another student.")
          return redirect("student_list")
        
        student.full_name = full_name
        student.email =email
        student.phone =phone
        student.course = course

        student.save()
        messages.success(request, "Student updated successfully!")
        return redirect("student_list")

    return render(
        request,
        "students/edit_student.html",
        {"student": student}
    )



