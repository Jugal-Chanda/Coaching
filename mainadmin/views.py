
from django.shortcuts import render,redirect
from accounts.models import User,Batch
from accounts import auth_fun
from accounts.forms import addBatchForm
# from accounts.models import Batch
from classlinks.forms import add_subject_form,add_class_time_form,add_class_form
from vedios.forms import add_vedio_form
from django.contrib import messages


def index(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            return render(request,'admin/index.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')

def add_batch(request):
    context={}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                form = addBatchForm(request.POST)
                if form.is_valid():
                    batch = form.save()
                    return redirect('all_batches')
                else:
                    context['form'] = form
            else:
                form = addBatchForm()
                context['form'] = form
            return render(request, 'admin/add_batch.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')


def all_batches(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            batches = Batch.objects.all()
            context['batches'] = batches
            return render(request,'admin/batches.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')


def students(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            context['students'] = User.objects.filter(is_student=True,student_aprove = True)
            return render(request,'admin/students.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')



def teachers(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            context['teachers'] = User.objects.filter(is_teacher=True,teacher_aprove = True)
            return render(request,'admin/teachers.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')


def subject_add(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                form = add_subject_form(request.POST)
                if form.is_valid():
                    subject = form.save()
                    messages.add_message(request, messages.SUCCESS, subject.name+' subject added successfully')
                    return redirect('subject_add')
            else:
                form = add_subject_form()
            context['form'] = form
            return render(request,'admin/add_subject.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')


def add_class(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                form = add_class_form(request.POST)
                if form.is_valid():
                    classlink = form.save()
                    messages.add_message(request, messages.SUCCESS, classlink.subject.name + " class added to " + classlink.subject.batch.name )
                    context['form'] =add_class_form()
                else:
                    context['form'] = form
            else:
                context['form'] = add_class_form()
            return render(request,'admin/add_class.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')


def add_class_time(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                form = add_class_time_form(request.POST)
                if form.is_valid():
                    classtime = form.save()
                    if classtime:
                        form = add_class_time_form()
                        messages.add_message(request, messages.SUCCESS, "Class time added to database")
                        return redirect('add_class_time')
            else:
                form = add_class_time_form()
            context['form'] = form
            return render(request,'admin/add_class_time.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')








def student_paid(request,id):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            user = User.objects.get(pk=id)
            if user:
                user.payment = True
                user.save()
            return redirect('students')
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')





def add_vedio(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                form = add_vedio_form(request.POST)
                if form.is_valid():
                    vedio = form.save()
                    messages.add_message(request, messages.SUCCESS, "Vedio added")
                    return redirect('add_vedio')
                else:
                    context['form'] = form
                    return redirect('add_vedio')
            else:
                context['form'] = add_vedio_form()
            return render(request,'admin/add_vedios.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')
