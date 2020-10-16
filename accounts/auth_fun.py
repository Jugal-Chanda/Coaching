from accounts.models import User
from django.shortcuts import render,redirect
from django.contrib import messages





def is_authenticate(user):
    if user.is_authenticated:
        return True
    return False

def admin_login(request):
    user = request.user
    if is_authenticate(user):
        if user.is_superadmin:
            return 'adminHome' # is and admin
        else:
            pass
    else:
        return 'login' # not authenticate


def student_login(request):
    user = request.user
    if is_authenticate(user):
        if user.is_student:
            if user.student_aprove:
                if user.payment:
                    return 'studenthome'
                else:
                    messages.add_message(request, messages.ERROR, 'Your payment is not completed')
                    return "error_page" # Payment Not completed
            else:
                messages.add_message(request, messages.ERROR, 'Your are not still aproved')
                return "error_page" # Student not aproved
        else:
            return False #Not a student account
    else:
        return 'login'

def teacher_login(request):
    user = request.user
    if is_authenticate(user):
        if user.is_teacher:
            # user has a teacher acco
            if user.teacher_aprove:
                # teacher aproved
                return 'teacherhome'
        else:
            # user donot have teacher account
            print("You donot have a teacher account")
    else:
        return 'login'


def redirect_permision(request):
    user = request.user
    if user.is_superadmin:
        return admin_login(request)
    elif user.is_student:
        return student_login(request)
    elif user.is_teacher:
        return teacher_login(request)
    else:
        messages.add_message(request, messages.ERROR, 'You Donot have any rule of this system. Please contact with admin')
        return "error_page"

# #
# # def club_per(user):
# #     if is_authenticate(user):
# #         if user.is_ec:
# #             club_ec = Club_Ec.objects.get(ec=user)
# #             club = Clubs.objects.get(pk=club_ec.club_id)
# #             if club.is_active:
# #                 return True
# #             else:
# #                 return False
# #         else:
# #             return False
# #     else:
# #         return False
# #
# # def admin_per(user):
# #     if is_authenticate(user):
# #         if user.is_admin:
# #             return True
# #         else:
# #             return False
# #     else:
# #         return False
