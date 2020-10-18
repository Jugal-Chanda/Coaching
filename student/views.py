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
            days = ['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
            context['days'] = days # for table heading render days
            context['user'] = request.user

            user = request.user
            # Selecting all subject according to batch
            batch = user.batch
            subjects = batch.subject_set.all()
            context['subjects'] = subjects # For showing vedios we need to render subjects also

            # Getting all classlinks according to subject for next 1 weeks
            today_date = date.today()
            after_week = today_date + timedelta(6)
            classlinks = ClassLink.objects.none()
            for subject in subjects:
                temp = subject.classlink_set.filter(classdate__gte = today_date,classdate__lte = after_week)
                classlinks = classlinks | temp

            # Making classroutine. Every cell contains a classlink object
            classroutine = {}
            for classlink in classlinks:
                d = days.index(classlink.classdate.strftime("%a")) # find the index number from days array based on classdate day
                t = classlink.classtime
                if t in classroutine.keys():
                    classroutine[t][d] = classlink
                else:
                    classroutine[t] = ["" for i in range(7)] # if classtime not in classroutine keys values then initiate a list for this classtime
                    classroutine[t][d] = classlink
            context['classroutine'] =  classroutine

            return render(request,'students/index.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')
