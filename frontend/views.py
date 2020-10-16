from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'index.html',{})
def error_page(request):
    return render(request,'error.html',{})
