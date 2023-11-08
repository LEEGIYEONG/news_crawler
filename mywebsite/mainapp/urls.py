from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('space/', views.space, name='space'), 
    path('semiconductor/', views.semiconductor, name='semiconductor'),
    path('hydrogen/', views.semiconductor, name='hydrogen'),
    path('ai/', views.semiconductor, name='ai'),
    path('robot/', views.semiconductor, name='robot'),
    path('battery/', views.semiconductor, name='battery'),

]