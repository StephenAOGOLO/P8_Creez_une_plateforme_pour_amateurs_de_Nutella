""" This module handle the urls of the application.
 It precise the format to use, the views function to call and a name.  """
from django.urls import path


from . import views

APP_NAME = "substitute"
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.homepage, name='home'),
    path('search/product=<str:product>', views.search, name='search'),
    path('aliment/S=<str:s_id>&P=<str:p_id>&U=<str:u_id>/', views.aliment, name='aliment'),
    path('save/P=<str:p_id>&S=<str:s_id>&U=<str:u_id>/', views.save, name='save'),
    path('account/', views.account, name='account'),
    path('historic/', views.historic, name='historic'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mentions/', views.mentions, name='mentions'),
]
