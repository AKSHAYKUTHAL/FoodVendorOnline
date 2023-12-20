from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('profile/',views.v_profile, name='v_profile'),

]