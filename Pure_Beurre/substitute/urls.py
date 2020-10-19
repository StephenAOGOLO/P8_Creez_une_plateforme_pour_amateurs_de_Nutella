from django.urls import path


from . import views

app_name = "substitute"
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.homepage, name='home'),
    path('results/', views.results, name='results'),
    path('aliment/', views.aliment, name='aliment'),
    path('account/', views.account, name='account'),
]
