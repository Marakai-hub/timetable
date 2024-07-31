from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_view, name='timetable'),
    path('general/', views.general_timetable_view, name='general_timetable_view'),
     
]
