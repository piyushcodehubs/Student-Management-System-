from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
  # return HttpResponse("hello")
  return render(request,"students/home.html")

def services(request):
  return render(request, "students/Services.html")