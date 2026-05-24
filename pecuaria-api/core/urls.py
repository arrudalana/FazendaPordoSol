from django import views
from django.contrib import admin
from django.urls import path, include
from api import views as api_views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/login/')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('login/', api_views.realizar_login, name='login_page'),
]