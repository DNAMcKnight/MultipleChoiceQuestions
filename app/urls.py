from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('generate', views.generate, name='generate'),
    path('reset', views.reset, name='reset'),
    path('export', views.export, name='export'),
    path('import', views.importData, name='import'),
]
