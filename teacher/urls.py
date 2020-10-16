from django.urls import path,include
from teacher import views


urlpatterns = [
    path('index/', views.index, name='teacherhome'),
    path('pending/', views.teachers_pending, name='teachers_pending'),
    path('aprove/<int:id>',views.aprove_teacher,name='aprove_teacher'),

]
