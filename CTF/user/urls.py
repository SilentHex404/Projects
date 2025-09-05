from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('profile/',views.Profile,name='profile'),
    path('logout/',views.Logout,name='logout'),
    path('UpdateProfile/',views.UpdateProfile,name='UpdateProfile'),
    path('ChangePassword/',views.ChangePassword,name='ChangePassword'),
]
