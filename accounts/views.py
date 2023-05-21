from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .forms import LoginForm
from django.http import HttpResponse

# Create your views here.
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
                    return HttpResponse('authenticated')
                else:
                    return HttpResponse('Disabled accounts')
            else:
                return HttpResponse('Invalid Credentials')
    else:
        form=LoginForm()
    context={'form':form}
    return render(request,'accounts/login.html',context)


def dashboard(request):
    return render(request,'accounts/dashboard.html')
