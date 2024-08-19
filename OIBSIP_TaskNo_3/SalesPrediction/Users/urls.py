from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='homepage'),
  
    path('predict',views.predict,name='predictpage')
]