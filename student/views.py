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
                    batches = Batch.objects.filter(capacity__gt = 0)
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
            context['days'] = days # For table Heading render this

            context['user'] = request.user
            user = request.user
            #Select all subject according to user batch
            batch = user.batch
            subjects = batch.subject_set.all()
            context['subjects'] = subjects # For vedios we need to render it also

            # get all classlinks according to subjects  wchich is from today to next 1 week
            classlinks = ClassLink.objects.none()
            today_date = date.today()
            after_week = today_date + timedelta(6)

            for subject in subjects:
                temp = subject.classlink_set.filter(classdate__gte = today_date,classdate__lte = after_week)
                classlinks = classlinks | temp

            # Makign classroutine that contains classtime as a key and in every cell contains a classlink
            classroutine = {}
            for classlink in classlinks:
                d = days.index(classlink.classdate.strftime("%a")) # find the days index from days list
                t = classlink.classtime
                if t in classroutine.keys():
                    classroutine[t][d] = classlink
                else:
                    classroutine[t] = ["" for i in range(7)]
                    classroutine[t][d] = classlink


            context['classroutine'] =  classroutine

            return render(request,'students/index.html',context)
        else:
            return redirect(auth_fun.redirect_permision(request))
    else:
        return redirect('login')
