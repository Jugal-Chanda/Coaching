from django.urls import path,include
from vedios import views

urlpatterns = [
    path('students/vedios/<int:id>/',views.vedio_links_students,name="vedio_links_students"),
    path('teachers/vedios/<int:id>/',views.vedio_links_teachers,name="vedio_links_teachers"),
    path('ajax/batch/subjects',views.batch_to_subjects,name="batch_to_subjects"),
    path('ajax/subject/classlinks',views.subject_to_classlink,name ="subject_to_classlink"),
]
