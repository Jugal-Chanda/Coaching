from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from accounts.forms import RegistrationForm,Log_in_Form
from accounts.models import User
from django.contrib import messages
from accounts import auth_fun


def register_student(request):
    context={}
    if request.POST:
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()
            # login(self.request, user)
            return redirect('login')
        else:
            context['form'] = form
    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'accounts/student_register.html',context)

def register_teacher(request):
    context={}
    if request.POST:
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_teacher = True
            user.save()
            # login(self.request, user)
            return redirect('login')
        else:
            context['form'] = form
    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'accounts/teacher_register.html',context)


def login_view(request):
    context={}
    user = request.user
    if auth_fun.is_authenticate(user):
        return redirect(auth_fun.redirect_permision(request))
    else:
        if request.POST:
            form = Log_in_Form(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(email=email,password=password)
                if user:
                    login(request,user)
                    if auth_fun.is_authenticate(user):
                        return redirect(auth_fun.redirect_permision(request))
                else:
                    messages.add_message(request, messages.ERROR, 'Invalid Login')
        else:
            form = Log_in_Form()
        context['form'] = form
    return render(request, 'accounts/login.html',context)





    # if auth_fun.is_authenticate(request.user):
    #         return redirect(auth_fun.redirect_permision(request.user))
    # if request.POST:
    #     form = Log_in_Form(request.POST)
    #     if form.is_valid():
    #         email = form.cleaned_data.get('email')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(email=email,password=password)
    #         if user:
    #             login(request,user)
    #             return redirect(redirect_permisions(user))
    #         else:
    #             messages.add_message(request, messages.ERROR, 'Invalid Login Try Again')
    #
    # else:
    #     form = Log_in_Form()
    # context['form'] = form
    # return render(request, 'accounts/login.html',context)
#
#
def logout_view(request):
    logout(request);
    # form = Log_in_Form()
    return redirect('login')
