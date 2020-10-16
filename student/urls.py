from django.urls import path,include
from student import views


urlpatterns = [
    path('index/', views.index, name='studenthome'),
    path('pending/', views.students_pending, name='students_pending'),
    path('aprove/view/<int:id>',views.aprove_student,name='aprove_student'),
    path('delete/<int:id>',views.delete_student,name="delete_student"),
]
