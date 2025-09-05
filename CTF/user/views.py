from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User

def Register(request) :
    if request.user.is_authenticated :
        return redirect('challenges')
    if request.method == 'POST' :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password :
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() :
                messages.error(request , 'نام کاربری یا ایمیل قبلا گرفته شده است')
            else :
                if len(password) >= 8 :
                    user = User.objects.create_user(username=username , email=email , password=password)
                    messages.success(request,'ثبت نام با موفقیت انجام شد')
                    return redirect('login')
                else :
                    messages.error(request,'رمز عبور باید حداقل 8 کاراکتر باشد')
        else :
            messages.error(request,'فیلد ها نباید خالی باشند')
    return render(request , 'user/register.html')


def Login(request) :
    if request.user.is_authenticated :
        return redirect('challenges')
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password :
            user = authenticate(request , username=username , password=password)
            if user :
                login(request , user)
                return redirect('challenges')
            else :
                messages.error(request , 'نام کاربری یا رمز عبور اشتباه است')
        else :
            messages.error(request,'نام کاربری و رمز عبور نباید خالی باشند')
    return render(request , 'user/login.html')

@login_required
def Logout(request) :
    logout(request)
    return redirect('login')   
    
@login_required(login_url="login")
def Profile(request) :
    return render(request , 'user/profile.html')

@login_required(login_url='login')
def UpdateProfile(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        if new_username:
            if new_username == request.user.username :
                messages.error(request,'نام کاربری یکسان است')
            elif User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
                messages.error(request, 'نام کاربری وارد شده وجود دارد')
            else:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'نام کاربری با موفقیت تغییر کرد')
        else:
            messages.error(request, 'نام کاربری نمی‌تواند خالی باشد')
        return redirect('profile')
    return render(request, 'user/profile.html')

@login_required(login_url='login')
def ChangePassword(request) :
    if request.method == 'POST' :
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        if current_password and new_password :
            if request.user.check_password(new_password) :
                messages.error(request,'رمز عبور جدید باید متفاوت باشد')
            else :
                if request.user.check_password(current_password):
                    if len(new_password) >= 8 :
                        request.user.set_password(new_password)
                        request.user.save()
                        messages.success(request,'رمز عبور با موفقیت تغییر کرد')
                        logout(request)
                        return redirect('login')
                    else :
                        messages.error(request , 'رمز عبور جدید باید حداقل 8 کاراکتر باشد')
                else :
                    messages.error(request,'رمز عبور فعلی برابر نیست')
        else :
            messages.error(request,'تمام فیلد ها را وارد کنید')
        return redirect('profile')
    else :
        return render(request , 'user/profile.html')