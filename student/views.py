from django.shortcuts import render,redirect
from accounts.models import User,Batch
from accounts import auth_fun
from classlinks.models import Classtime,ClassLink,Subject
from datetime import datetime, timedelta,date
# # Create your views here.
# #**********  Student View **********************
# #==============================================
#

def students_pending(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            context['students'] = User.objects.filter(is_student = True).exclude(student_aprove=True)
            return render(request,'admin/students_pending.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')



def aprove_student(request,id):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            if request.POST:
                user = User.objects.get(pk=request.POST.get('user_id'))
                if user:
                    batch = Batch.objects.get(pk=request.POST.get('batch_id'))
                    if batch:
                        user.batch = batch
                        user.student_aprove = True
                        user.save()
                        batch.enrolled+=1
                        batch.save()
                        return redirect('students_pending')
                    else:
                        #Batch not found
                        messages.add_message(request, messages.ERROR, 'batch not found. Something went to wrong')

                else:
                    messages.add_message(request, messages.ERROR, 'User not found. Something went to wrong')
                    return  redirect('error_page') #user Not found
            else:
                user = User.objects.get(pk=id)
                if user:
                    context['user'] = user
                    batches = Batch.objects.filter(capacity__gt = enrolled)
                    context['batches'] = batches
                else:
                    messages.add_message(request, messages.ERROR, 'User not found. Something went to wrong')
                    return  redirect('error_page') #user Not found
            return render(request,'admin/aprove_student.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')



def delete_student(request,id):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'adminHome':
            user = User.objects.get(pk=id)
            if user:
                user.delete()
            return redirect('students')
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')


def index(request):
    context = {}
    if auth_fun.is_authenticate(request.user):
        if auth_fun.redirect_permision(request) == 'studenthome':
            classtimes_temp = Classtime.objects.all()

            classtimes_index = []
            classtimes = []

            for classtime in classtimes_temp:
                classtimes_index.append(classtime.id)
                classtimes.append(classtime)

            context['classtimes'] = classtimes

            context['user'] = request.user
            user = request.user
            batch = user.batch
            subjects = batch.subject_set.all()

            classlinks = ClassLink.objects.none()
            today_date = date.today()
            after_week = today_date + timedelta(6)

            for subject in subjects:
                temp = subject.classlink_set.filter(classdate__gte = today_date,classdate__lte = after_week)
                classlinks = classlinks | temp

            l = len(classtimes_index)
            days = ['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
            classroutine = {}
            for day in days:
                classroutine[day] = ["" for i in range(l)]
            for classlink in classlinks:
                d = classlink.classdate.strftime("%a")
                t = classtimes_index.index(classlink.classtime.id)
                classroutine[d][t] = classlink

            context['days'] = days
            context['classroutine'] =  classroutine
            context['subjects'] = subjects
            return render(request,'students/index.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')
