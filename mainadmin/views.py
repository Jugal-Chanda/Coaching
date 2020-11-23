from django.shortcuts import render,redirect
from accounts.models import User,Batch
from accounts import auth_fun
from accounts.forms import addBatchForm
from classlinks.forms import add_class_time_form
from vedios.models import Vedio
from django.contrib import messages
from classlinks.models import ClassLink,Subject,Classtime
from notices.forms import add_notice_form
from notification import notify
from mainadmin.helper_func import check_techer_panding,check_student_panding
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from datetime import datetime, timedelta,date


def add_notice(request):
    context = {}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()

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
    context['students'] = User.objects.filter(is_student=True).count()
    context['teachers'] = User.objects.filter(is_teacher=True).count()
    context['classes'] = ClassLink.objects.filter(classdate=date.today())
    context['vedios'] = Vedio.objects.filter(created_at=date.today())
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':

            return render(request,'admin/index.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')

def add_batch(request):
    context={}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                form = addBatchForm(request.POST)
                if form.is_valid():
                    batch = form.save()
                    if request.POST.get('next', ''):
                        request.session['batch'] = batch.id
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
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
                    request.session['pre_subject'] = subject.id
                    request.session['pre_batch'] = subject.batch.id
                    message  = ""
                for req_subject in req_subjects:
                    message+= req_subject+', '
                messages.add_message(request, messages.SUCCESS, message + " Subjects added ")
                if request.POST.get('next',''):
                    return redirect('assign_teacher_and_add_url')

            else:
                context['batches'] = Batch.objects.all()
                if request.session.get('batch',''):
                    context['pre_batch'] = request.session['batch']
                else:
                    context['pre_batch'] = 0
            return render(request,'admin/add_subject.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')

def batch_wise_subjects(request,batch):
    context = {}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    batch = Batch.objects.get(pk=batch)
    context['batch'] = batch
    context['subjects'] = batch.subject_set.all()
    return render(request,'admin/subjects.html',context)

def assign_teacher_and_add_url(request):
    context = {}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    context['batches'] = Batch.objects.all()
    context['teachers'] = User.objects.filter(is_teacher=True,teacher_aprove=True,is_active=True)
    context['pre_batch'] = 0
    context['pre_subject'] = 0
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
                    return redirect('add_class_time')
            else:
                if request.session.get('pre_subject','') and request.session.get('pre_batch',''):
                    context['pre_batch'] = request.session.get('pre_batch','')
                    context['pre_subject'] = request.session.get('pre_subject','')
                    context['subjects'] = Batch.objects.get(pk=context['pre_batch']).subject_set.all()
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    context['batches'] = Batch.objects.all()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                subject = Subject.objects.get(pk=request.POST.get('subject'))
                classdate = datetime.strptime(request.POST.get('date'),'%d/%m/%Y').date()
                classtime = Classtime.objects.get(pk = request.POST.get('classtime') )
                classlink = ClassLink()
                classlink.subject = subject
                classlink.classdate = classdate
                classlink.classtime = classtime
                classlink.save()
                messages.add_message(request, messages.SUCCESS, classlink.subject.name + " class added to " + classlink.subject.batch.name )
                batch = classlink.subject.batch
                students = batch.user_set.all()
                msg = classlink.subject.name + " class link is added "
                notify.send(msg=msg,users=students)
            else:
                if request.session.get('pre_batch','') and request.session.get('pre_subject','') and request.session.get('pre_classtime',''):
                    batch = Batch.objects.get(pk = request.session['pre_batch'])
                    context['subjects'] = batch.subject_set.all()
                    context['pre_batch'] = request.session['pre_batch']
                    context['pre_subject'] = request.session['pre_subject']
                    context['pre_classtime'] = request.session['pre_classtime']
                    
                    del request.session['pre_batch']
                    del request.session['pre_subject']
                    del request.session['pre_classtime']
                context['batches'] = Batch.objects.all()
                context['classtimes'] = Classtime.objects.all()
            return render(request,'admin/add_class.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')

def add_class_time(request):
    context = {}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                form = add_class_time_form(request.POST)
                if form.is_valid():
                    classtime = form.save()
                    request.session['pre_classtime'] = classtime.id
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
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
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
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
