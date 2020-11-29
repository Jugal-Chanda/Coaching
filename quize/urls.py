from django.urls import path,include
from quize import views

# path('admin/', include('mainadmin.urls')),

urlpatterns = [
    path('', views.index, name='quize'),
]
