from accounts.models import User

def check_techer_panding():
    return User.objects.filter(is_teacher=True,teacher_aprove=False).count()
def check_student_panding():
    return User.objects.filter(is_student=True,student_aprove=False).count()
