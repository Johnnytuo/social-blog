from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from socialnetwork.forms import LoginForm, RegisterForm,EditForm

# Create your views here.

def login_action(request):
    context={}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request,"socialnetwork/login.html",context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render (request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    
    return redirect(reverse('post'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, "socialnetwork/register.html",context)

    form = RegisterForm(request.POST)
    context['form'] =form
    if not form.is_valid():
        return render(request,"socialnetwork/register.html", context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('post'))

def post_action(request):
    context = {}
    if request.method =='GET':
        return render(request,"socialnetwork/globalstream.html",context)

    return render(request,"socialnetwork/globalstream.html",context)

def profile_action(request):
    context ={}
    if request.method =='GET':
        return render(request,"socialnetwork/profile.html",context)

    return render(request, "socialnetwork/profile.html", context)

def followStream_action(request):
    context ={}
    if request.method =='GET':
        return render(request,"socialnetwork/followerstream.html",context)

    return render(request, "socialnetwork/followerstream.html", context)



def follower_action(request):
    context ={}
    if request.method =='GET':
        id=request.GET['id']
        entry = lookup_entry(id)
        form = EditForm(entry)
        context={'entry':entry,'form':form}
        return render(request,"socialnetwork/follower.html",context)





def lookup_entry(id):
    if (id == '1'):
        return Tony_Stark
    if (id == '2'):
        return Steve_Rogers
    if (id == '3'):
        return Peter_Parker
    return None


Tony_Stark= {
    'id': '1',
    'username': 'Tony_Stark',
    'last_name':    'Tony',
    'first_name':   'Stark',
    'email':      'Tony_Stark@Avengers.com',

}

Steve_Rogers= {
    'id': '2',
    'username': 'Steve_Rogers',
    'last_name':    'Steve',
    'first_name':   'Rogers',
    'email':        'Steve_Rogers@Avengers.com',
}


Peter_Parker={
     'id': '3',
     'username': 'Peter_Parker',
     'last_name': 'Peter',
     'first_name': 'Parker',
     'email': 'Peter_Parker@Avengers.com',
}





