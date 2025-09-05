from django.shortcuts import render,redirect
from django.db.models import Sum
from team.models import Team

def Home(request) :
    if request.user.is_authenticated :
        return redirect('challenges')
    return render(request,'home/home.html')

def Scoreboard(request):
    context = {}
    teams = Team.objects.all().annotate(total_score=Sum('team_members__score')).order_by('-total_score')
    context = {
        'teams': teams
    }
    return render(request, 'home/scoreboard.html', context)