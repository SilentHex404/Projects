from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import User
from .models import Team
import uuid

@login_required(login_url='login')
def CreateTeam(request) :
    if request.method == 'POST' :
        team_name = request.POST.get('team_name')
        team_desciption = request.POST.get('team_desciption')
        if team_name and team_desciption :
            if Team.objects.filter(name=team_name).exists() :
                messages.error(request,'تیم با نام وارد شده وجود دارد')
            else :
                creator = request.user
                if creator.team :
                    messages.error(request,'در حال حاضر در تیم حضور دارید')
                else :
                    created_team = Team.objects.create(name=team_name,description=team_desciption,manager=creator)
                    request.user.team = created_team
                    request.user.save()
                    messages.success(request,'تیم شما با موفقیت تشکیل شد')
        else :
            messages.error(request,'نام تیم و توضیحات تیم باید پر باشند')
        return redirect('team')
    else :
        return redirect('team')
    
    
@login_required(login_url='login')
def InviteUser(request) :
    if request.method == 'POST' :
        invite_code = request.POST.get('invite_code') 
        if invite_code :
            try :
                valid_code = uuid.UUID(invite_code)
            except (ValueError, TypeError) :
                messages.error(request,'کد دعوت معتبر نیست')
                return redirect('team')
            target = Team.objects.filter(id=invite_code).exists()
            if target :
                target_team = Team.objects.get(id=invite_code)
                user = request.user
                if user.team :
                    messages.error(request,'شما در تیم حضور دارید')
                else :
                    request.user.team = target_team
                    request.user.save()
                    messages.success(request,f'شدید {target_team.name} شما با موفقیت وارد تیم')
            else :
                messages.error(request,'تیم مورد نظر یافت نشد')
        else :
            messages.error(request,'کد دعوت را وارد کنید')
        return redirect('team')
    else :
        return redirect('team')
    
    

@login_required(login_url='login')
def ViewTeam(request) :
    context = {}
    user = request.user
    if user.team :
        team = user.team
        members = team.team_members.all()
        context = {
        'team':team,
        'members':members,
        }
    return render(request , 'team/team.html',context)

@login_required(login_url='login')
def TeamSettings(request):
    updated = False
    user = request.user
    team = user.team
    if not team :
        return redirect('team')
    else :
        if team.manager != user:
            return redirect('team')
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        team_description = request.POST.get('team_description')
        if team_name:
            if team_name == team.name :
                messages.error(request,'نام جدید با نام فعلی تیم برابر است')
            else :
                if Team.objects.filter(name=team_name).exclude(id=team.id).exists():
                    messages.error(request, 'نام تیم گرفته شده است')
                else:
                    team.name = team_name
                    updated = True
                    
        if team_description:
            if team_description == team.description :
                messages.error(request,'توضیحات تیم با توضیحات فعلی برابر است')
            else :
                team.description = team_description
                updated = True
        if updated :
            team.save()
            messages.success(request,'اطلاعات تیم با موفقیت تغییر کرد')
        return redirect('TeamSettings')
    members = team.team_members.all().exclude(id=user.id)
    
    context = {
        'team': team,
        'members':members
    }
    return render(request, 'team/TeamSettings.html', context)

@login_required
def RemoveUser(request) :
    user = request.user
    team = user.team
    if team :
        if team.manager != user :
            return redirect('team')
    if request.method == 'POST' :
        user_id = request.POST.get('user_id')
        if user_id :
            check = team.team_members.filter(id=user_id).exists()
            if check :
                try :
                    user_uuid = uuid.UUID(user_id)
                except (ValueError,TypeError) :
                    messages.error(request,'مقدار وارد شده صحیح نیست')
                    return redirect('TeamSettings')
                if user_uuid != team.manager.id :
                    user = User.objects.get(id=user_id)
                    user.team = None
                    user.save()
                    messages.success(request,f'با موفقیت از تیم حذف شد {user.username } کاربر')
                else :
                    messages.error(request,'نمیتوانید خودتان را حذف کنید')
            else :
                messages.error(request,'کاربر یافت نشد')
        return redirect('TeamSettings')
    else :
        return redirect('TeamSettings')