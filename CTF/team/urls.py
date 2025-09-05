from django.urls import path
from . import views

urlpatterns = [
    path('team/',views.ViewTeam,name='team'),
    path('TeamSettings/',views.TeamSettings,name='TeamSettings'),
    path('CreateTeam/',views.CreateTeam,name='CreateTeam'),
    path('InviteUser/',views.InviteUser,name='InviteUser'),
    path('RemoveUser/',views.RemoveUser,name='RemoveUser')
]
