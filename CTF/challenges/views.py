from django.shortcuts import render,redirect,get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Challenge , SolvedChallenge
import os

def challenges(request) :
    challs = Challenge.objects.all()
    solved_ids = SolvedChallenge.objects.filter(solved_by=request.user).values_list("challenge_id", flat=True)
    context = {
        'challs':challs,
        'solved_ids':solved_ids
    }
    return render(request , 'challenges/challenges.html',context)

@login_required(login_url='login')
def Chall(request, id):
    context = {}
    try:
        target = Challenge.objects.get(id=id)
        first_blood_record = SolvedChallenge.objects.filter(challenge=target).order_by("solved_at").first()
        first_blood_user = first_blood_record.solved_by if first_blood_record else None

        context = {
            'target': target,
            'first_blood_user': first_blood_user,
        }
    except Challenge.DoesNotExist:
        messages.error(request,'چالش مورد نظر یافت نشد')
        return redirect('challenges')
    
    return render(request, 'challenges/chall.html', context)

@login_required(login_url='login')
def DownloadFile(request, id):
    chall = get_object_or_404(Challenge, id=id)
    if not chall.ChallFile:
        messages.error(request, 'این چالش فایل برای دانلود ندارد')
        return redirect(f'/chall/{chall.id}')
    file_path = chall.ChallFile.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        messages.error(request, 'فایل مورد نظر یافت نشد.')
        return redirect(f'/chall/{chall.id}')


@login_required(login_url='login')
def SubmitFlag(request):
    if request.method == 'POST':
        chall_id = request.POST.get('chall_id')
        flag = request.POST.get('flag')

        if not chall_id or not flag:
            return redirect('challenges')

        try:
            target = Challenge.objects.get(id=chall_id)
        except Challenge.DoesNotExist:
            messages.error(request,'چالش مورد نظر پیدا نشد')
            return redirect('challenges')

        user = request.user
        
        if target.creator == user :
            messages.warning(request,'شما خودتان نمیتوانید چالش خودتان را حل کنید')
            return redirect(f'/chall/{target.id}')

        if target.solved_by.filter(id=user.id).exists():
            messages.warning(request,'شما این چالش را قبلا حل کرده اید')
            return redirect(f'/chall/{target.id}/')

        if target.flag == flag:
            if not target.solved_by.exists():
                user.first_bloods += 1
            target.solved_by.add(user)
            user.solved_challs += 1
            user.score += target.score
            user.save()
            messages.success(request,'چالش با موفقیت حل شد')
        else:
            messages.error(request,'فلگ اشتباه است')

        return redirect(f'/chall/{target.id}/')

    return redirect('challenges')


@login_required(login_url='login')
def CreateChall(request) :
    if request.method == 'POST' :
        chall_name = request.POST.get('chall_name')
        chall_desc = request.POST.get('chall_desc')
        
        try :
            score = int(request.POST.get('score'))
        except (ValueError,TypeError) :
            messages.error(request,'فیلد هارا با دقت و درست پر کنید')
            return redirect('profile')
        
        chall_file = request.FILES.get('chall_file')
        flag = request.POST.get('flag')
        
        if not chall_name or not chall_desc or not score or not chall_file or not flag :
            messages.error(request,'تمام فیلد ها را پر کنید')
            return redirect('profile')
        
        ext = chall_file.name.split('.')[-1].lower()
        if ext != 'zip':
            messages.error(request,'فایل باید فرمت zip داشته باشد')
            return redirect('profile')
        if Challenge.objects.filter(name=chall_name).exists() :
            messages.error(request,'نام چالش قبلا گرفته شده است')
            return redirect('profile')
        
        user = request.user
        
        Challenge.objects.create(name=chall_name,description=chall_desc,score=score,creator=user,flag=flag,ChallFile=chall_file)
        user.created_challs += 1
        user.save()
        messages.success(request,'چالش شما با موفقیت ساخته شد')
        
        return redirect('profile')
    else :
        return redirect('profile')