from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View




# 邮箱
from django.contrib.auth.hashers import make_password

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm,UserForm, UserProfileForm


from .models import EmailVerifyRecord, UserProfile
from django.contrib.auth.decorators import login_required

from utils.email_send import send_register_email
import datetime




class MyBackend(ModelBackend):
    '''邮箱登录注册'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):   # 加密明文密码
                return user
        except Exception as e:
            return None


def Actice_user(request, active_code):
    '''  修改用户状态，比对链接验证码'''
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for recod in all_records:
            email = recod.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save
    else:
        return HttpResponse("链接有误！")
    return redirect('user:login')




# Create your views here.

def Login(request):
    # if request.method =='POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     print(username,password)
    #
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return HttpResponse('登录成功!')
    #     else:
    #         return HttpResponse('登录失败!')
    # return render(request, 'user/login.html')

    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:user_profile')
            else:
                return HttpResponse('登录失败!')
    context = {'form': form}
    return render(request, 'user/login.html', context)

def Register(request):
    '''注册视图'''
    if request.method != 'POST':
        form = RegisterForm()
    else:
        pass
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = form.cleaned_data.get('email')
            new_user.save()

            # 发送邮件
            send_register_email(form.cleaned_data.get('email'), 'register')

            return HttpResponse('注册成功')

    context = {'form': form}
    return render(request, 'user/register.html', context)


def Forget_pwd(request):
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            exists = User.objects.filter(email=email).exists()
            if exists:
                #发送邮件
                send_register_email(email, 'forget')
                return HttpResponse('邮件已经成功发送，请查收!')
            else:
                return HttpResponse("邮箱尚未注册,请先前往注册!")
    return render(request, 'user/forget_pwd.html', {'form': form})


def forget_pwd_url(request, active_code):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('修改成功!')
        else:
            return HttpResponse('修改失败')
    return render(request, 'user/reset_pwd.html', {'form': form})

''' 设置登录后才能访问，如果没有登录跳转到登录界面'''
@login_required(login_url='users:login')
def user_profile(request):
    ''''''
    user = User.objects.get(username=request.user)
    return render(request, 'user/user_profile.html', {'user': user})

def Logout(request):
    '''  登出 '''
    logout(request)
    return redirect('user:login')

@login_required(login_url='user:login')
def editor_user(request):
    ''' 编辑用户信息 '''
    user = User.objects.get(id=request.user.id)  #当前登录用户
    if request.method == 'POST':
        try:
            # 如果userprofile
            userprofile = user.userprofile   # 如果这一数据不存在，会引发一个错误
    # UserProfile 和User之间是一个一对一的关系，默认注册 的时候为没有数据的，注册成功之后，他才会在个人中心设置信息

            # 第一次2登入的话应该是空表单，如果设置了数据，那以后编辑的话就是修改，一个要默认显示原有的数据
            form = UserForm(request.POST, instance=user) # 保存加修改的一个操作，instance默认显示它有原有的数据
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('user:user_profile')

        except UserProfile.DoesNotExist:
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()

                # commit= False 先不保存 先把数据保存在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据

                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                return redirect('user:user_profile')

    else:
        try:
            # 如果userprofile
            userprofile = user.userprofile  # 如果这一数据不存在，会引发一个错误

            form = UserForm(instance=user)  # 保存加修改的一个操作，instance默认显示它有原有的数据
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES)



    return render(request, 'user/editor_user.html',locals())