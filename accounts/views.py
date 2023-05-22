from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.http import HttpResponse
from .models import Profile
from django.contrib import messages

def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            username=cd['username']
            password=cd['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('/account/dashboard')
                else:
                    return HttpResponse('Disabled accounts')
            else:
                return HttpResponse('Invalid Credentials')
    else:
        form=LoginForm()
    context={'form':form}
    return render(request,'accounts/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('/account/login/')

def registerUser(request):
    if request.method=="POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'accounts/register_done.html',{'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request,'accounts/register.html',{'user_form':user_form})

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request,'accounts/dashboard.html',{'section':'dashboard'})
@login_required
def edit(request):
    if request.method=='POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated Successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    context={'user_form':user_form,'profile_form':profile_form}

    return render(request,'accounts/edit.html',context)

