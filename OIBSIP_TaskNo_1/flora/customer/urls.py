from django.urls import path
from .import views
urlpatterns=[
    path('index',views.index,name='home'),
    path('find',views.find,name='find')
]