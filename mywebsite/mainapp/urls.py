from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('space/', views.space, name='space'),
    path('semiconductor/', views.semiconductor, name='semiconductor'),
    path('hydrogen/', views.hydrogen, name='hydrogen'),
    path('ai/', views.ai, name='ai'),
    path('robot/', views.robot, name='robot'),
    path('battery/', views.battery, name='battery'),

]
