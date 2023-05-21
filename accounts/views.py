from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm
from django.http import HttpResponse

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
                    return redirect('/accounts/dashboard')
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
    return redirect('/accounts/login/')

def registerUser(request):
    if request.method=="POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.cleaned_data
            new_user.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'accounts/register_done.html',{'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request,'accounts/register.html',{'user_form':user_form})

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request,'accounts/dashboard.html',{'section':'dashboard'})
