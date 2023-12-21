from django.urls import path, include
from . import views
from accounts import views as AccountViews

app_name = "vendor"

urlpatterns = [
    path('',AccountViews.vendorDashboard, name='vendor'),
    path('profile/',views.v_profile, name='v_profile'),

]