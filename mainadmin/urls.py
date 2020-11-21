from django.urls import path,include
from mainadmin import views

# path('admin/', include('mainadmin.urls')),

urlpatterns = [
    path('index/', views.index, name='adminHome'),
    path('teachers/', views.teachers, name='teachers'),
    path('students/', views.students, name='students'),
    path('student/paid/<int:id>',views.student_paid,name="student_paid"),
    path('subject/add/',views.subject_add,name="subject_add"),


    path('batch/add/',views.add_batch,name="add_batch"),
    path('batches',views.all_batches,name="all_batches"),
    path('batches/<int:id>',views.batch_student,name="batch_student"),
    path('class/time/add',views.add_class_time,name="add_class_time"),
    path('class/add/',views.add_class,name="add_class"),

    path('vedio/add/',views.add_vedio,name="add_vedio"),

    path('notice/add/',views.add_notice,name="add_notice"),

    path('ajax/batch/subjects',views.ajax_batch_to_subjects,name="ajax_batch_to_subjects"),




]
