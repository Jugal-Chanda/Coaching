from django.urls import path,include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registration/student/', views.register_student, name='student_registration'),
    path('registration/teacher/', views.register_teacher, name='teacher_registration'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view,name="logout")
]
