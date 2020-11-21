from django.shortcuts import render,redirect
from accounts.models import User,Batch
from accounts import auth_fun
from accounts.forms import addBatchForm
from classlinks.forms import add_class_time_form,add_class_form
from vedios.models import Vedio
from django.contrib import messages
from classlinks.models import ClassLink,Subject
from notices.forms import add_notice_form
from notification import notify

from django.core import serializers
from django.http import HttpResponse,JsonResponse


def add_notice(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':

            if request.POST:
                form = add_notice_form(request.POST)
                if form.is_valid():
                    notice = form.save()
                    messages.add_message(request, messages.SUCCESS, notice.notice +' added successfully')
            else:
                form = add_notice_form()

            context['form'] = form
            return render(request,'admin/add_notice.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')

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
                    if request.POST.get('next', ''): # Check next btn is pressed or not
                        return redirect('subject_add')
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

def batch_student(request,id):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            batch = Batch.objects.get(pk=id)
            students = batch.user_set.all()
            context['students'] = students
            return render(request,'admin/batch_student.html',context)
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
                req_subjects = list(request.POST.get('subjects').split(','))
                req_batch = request.POST.get('batch')
                for req_subject in req_subjects:
                    subject = Subject()
                    subject.name = req_subject
                    subject.batch = Batch.objects.get(pk=req_batch)
                    subject.save()
                    message  = ""
                for req_subject in req_subjects:
                    message+= req_subject+', '
                messages.add_message(request, messages.SUCCESS, message + " Subjects added ")

            else:
                context['batches'] = Batch.objects.all()
            return render(request,'admin/add_subject.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')

def assign_teacher_and_add_url(request):
    context = {}
    context['batches'] = Batch.objects.all()
    context['teachers'] = User.objects.filter(is_teacher=True,teacher_aprove=True,is_active=True)
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                subject = request.POST.get('subject_select')
                teacher = request.POST.get('teacher')
                url = request.POST.get('url')
                subject = Subject.objects.get(pk=subject)
                subject.teacher = User.objects.get(pk=teacher)
                subject.url = url
                subject.save()
                messages.add_message(request, messages.SUCCESS, "Teacher and classlink added successfully")
                if request.POST.get('next',''):
                    return redirect('add_class')   
            return render(request,'admin/assign_teache_and_url.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')

def ajax_batch_to_subjects(request):
    data = {}
    if request.GET:
        batch_id = request.GET.get('batch_id')
        batch = Batch.objects.get(pk=batch_id)
        if batch:
            subjects = batch.subject_set.all()
            data = serializers.serialize('json', subjects)
        print(data)
    return JsonResponse(data,safe=False)

def add_class(request):
    context = {}
    context['batches'] = Batch.objects.all()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                # subject_id = request.POST.get('subject')
                # subject = Subject.objects.get('subject_id')
                form = add_class_form(request.POST)
                if form.is_valid():
                    classlink = form.save()
                    messages.add_message(request, messages.SUCCESS, classlink.subject.name + " class added to " + classlink.subject.batch.name )
                    batch = classlink.subject.batch
                    students = batch.user_set.all()
                    msg = classlink.subject.name + " class link is added "
                    notify.send(msg=msg,users=students)
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
                        messages.add_message(request, messages.SUCCESS, "Class time added to database")
                        form = add_class_time_form()
                        if request.POST.get('next', ''): # Check next btn is pressed or not
                            return redirect('add_class')
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
                classlink_id = request.POST.get('class')
                vedio_title = request.POST.get('title')
                vedio_url = request.POST.get('url')
                classlink = ClassLink.objects.get(pk=classlink_id)
                vedio = Vedio()
                vedio.classlink = classlink
                vedio.title = vedio_title
                vedio.url = vedio_url
                vedio.save()
                students = classlink.subject.batch.user_set.all()
                msg = classlink.subject.name +  " class recoding is added"
                notify.send(msg=msg,users=students)
                messages.add_message(request, messages.SUCCESS, "Vedio added")
                return redirect('add_vedio')
            else:
                context['batches'] = Batch.objects.all()
            return render(request,'admin/add_vedios.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')
