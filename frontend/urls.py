from django.urls import path,include
from frontend import views

# path('admin/', include('mainadmin.urls')),

urlpatterns = [
    path('',views.home,name="landingpage"),
    path('error',views.error_page,name="error_page")
]
