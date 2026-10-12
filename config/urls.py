from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('LEM.urls')),
    path('', include('dashboard.urls')),
    path('admin/', admin.site.urls),
]