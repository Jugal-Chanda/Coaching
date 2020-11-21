from django.shortcuts import render,redirect
from accounts.models import User
from accounts import auth_fun
from classlinks.models import Classtime,ClassLink,Subject
from datetime import datetime, timedelta,date
from mainadmin.helper_func import check_techer_panding,check_student_panding
#
#
# # Create your views here.
# # **************** Teacher View *********************
# #-=========================================================

def teachers_pending(request):
    context = {}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            context['teachers'] = User.objects.filter(is_teacher = True).exclude(teacher_aprove=True)
            return render(request,'admin/teachers_pending.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')
# teacherhome
def aprove_teacher(request,id):
    context = {}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            user = User.objects.get(pk=id)
            if user:
                user.teacher_aprove = True
                user.save()
            return redirect('teachers_pending')
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')






def index(request):
    context = {}
    context['teachers_pending'] = check_techer_panding()
    context['students_pending'] = check_student_panding()
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'teacherhome':
            classtimes_temp = Classtime.objects.all()
            classtimes_index = []
            classtimes = []
            for classtime in classtimes_temp:
                classtimes_index.append(classtime.id)
                classtimes.append(classtime)

            context['classtimes'] = classtimes

            context['user'] = request.user
            user = request.user
            today_date = date.today()
            after_week = today_date + timedelta(6)

            classlinks = user.classlink_set.filter(classdate__gte = today_date,classdate__lte = after_week)
            l = len(classtimes_index)
            days = ['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
            classroutine = {}
            for day in days:
                classroutine[day] = ["" for i in range(l)]

            subjects = []
            for classlink in classlinks:
                d = classlink.classdate.strftime("%a")
                t = classtimes_index.index(classlink.classtime.id)
                classroutine[d][t] = classlink
                if classlink.subject not in subjects:
                    subjects.append(classlink.subject)
            context['days'] = days
            context['classroutine'] =  classroutine
            context['subjects'] = subjects

            return render(request,'teachers/index.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')
