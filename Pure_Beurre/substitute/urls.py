from django.urls import path


from . import views

app_name = "substitute"
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.homepage, name='home'),
    path('search/product=<str:product>/', views.search, name='search'),
    path('aliment/<str:pk>/', views.aliment, name='aliment'),
    path('save/P=<str:p_id>&S=<str:s_id>&U=<str:u_id>/', views.save, name='save'),
    path('account/', views.account, name='account'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
