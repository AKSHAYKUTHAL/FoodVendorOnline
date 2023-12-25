from django.urls import path, include
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('',views.marketplace,name='marketplace'),
]