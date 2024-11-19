from django.contrib import admin
from django.urls import path, include   # Add


urlpatterns = [
    path('sample_app/', include('sample_app.urls')),   # Add
    path('admin/', admin.site.urls),
]