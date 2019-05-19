
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from socialnetwork.forms import LoginForm, RegisterForm,EditForm,ProfileForm,PostForm
from socialnetwork.models import *
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.







def login_action(request):
    context={}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request,"socialnetwork/login.html",context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

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

    new_user_profile = Profile(user=new_user)
    new_user_profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

@ensure_csrf_cookie
@login_required
def post_action(request):
    errors =[]
    context = {}
    form = PostForm(request.POST)
    if not form.is_valid():
        context['form'] = form
    # if request.method =='GET':
    #     form = PostForm()
    #     context['forms'] = form

    #     return render(request,"socialnetwork/globalstream.html",context)
    # elif 'post' not in request.POST or not request.POST['post']:
    #     errors.append("You must enter an item to post.")
    else:

        new_post = Post(post_text = form.cleaned_data['post_text'],
                        user = request.user,
                        time = timezone.now()
                        )
        form = PostForm(request.POST,instance = new_post)
        form.save()
    context['forms'] = PostForm()
    # context['errors'] = errors
    posts = Post.objects.all().order_by('-time', 'id')
    context['posts'] = posts

    return render(request,"socialnetwork/globalstream.html",context)





def profile_action(request,id):

    context ={}
    id = int(id)

    if id != request.user.id:
        followee_profile = Profile.objects.filter(user_id=id).last()
        request_user_profile = Profile.objects.filter(user_id=request.user.id).last()

        context['followee_profile']=followee_profile
        context['user_profile'] = request_user_profile
        try:
            context['followers'] = request_user_profile.followers.all()
        except:
            context['followers'] =None
        return render(request,"socialnetwork/follower.html",context)

    new_profile = Profile.objects.filter(user_id=request.user.id).last()
    form = ProfileForm(request.POST,request.FILES)
        # request.POST, request.FILES, instance=new_profile)

    if not form.is_valid():
        context['form'] = form
        # temp = Profile.objects.all()
        try:
            # stuck by this!!!:
            # objects.get() can only get one qualified,so if there many same user, it will failed
            # So I use filter which can get all qualified user, and choose the last one which updated recently
            context['profile']=Profile.objects.filter(user=request.user).last()
            context['followers'] = new_profile.followers.all()

        except:
            context['followers'] = None

        return render(request, "socialnetwork/profile.html", context)

    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        context['form'] = form
        pic = form.cleaned_data['profile_picture']
        print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
        new_profile.profile_picture = pic
        new_profile.content_type = form.cleaned_data['profile_picture'].content_type
        new_profile.bio_text = request.POST['bio_text']
        new_profile.save()
        context['profile'] = new_profile
        context['followers'] = new_profile.followers.all()
    return render(request, "socialnetwork/profile.html", context)
        # new_profile = form.save(commit = False)
        # new_profile.user = request.user
        # new_profile.save()
        # context['message'] = 'Item #{0} saved.'.format(new_profile.id)
        # context['form'] = ProfileForm()
    # context['profile'] = Profile.objects.get(id=new_profile.id)
    # profiles= Profile.objects.all()
    # for profile in profiles:
    #     if profile.id != new_profile.id or profile.id is None:
    #         profile.delete()
    # context['profiles'] = profiles

    # p=Profile.objects.all()

    # try :
    #     context['profile'] = Profile.objects.get(user_id=request.user.id)
    # except:
    #     context['profile'] = None




def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, profile.profile_picture, type(profile.profile_picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not profile.profile_picture:
        raise Http404
    return HttpResponse(profile.profile_picture, content_type=profile.content_type)




def follow_action(request,id):
    context ={}
    followee = User.objects.get(id=id)
    followee_profile = Profile.objects.filter(user_id=id).last()
    try:
        request_user_profile = Profile.objects.filter(user=request.user).last()
    except:
        request_user_profile = None
    # if followee not in request_user_profile.followers:
    request_user_profile.followers.add(followee)
    request_user_profile.save()
    # request_user_profile.save()
    follower= request_user_profile.followers.all()
    # if followee in user:
    #     print("t")
    # else:
    #     pass

    followee_profile = Profile.objects.filter(user_id=id).last()
    context={'user_profile':request_user_profile,'followee_profile':followee_profile,'followers':follower}

    return render(request,"socialnetwork/follower.html", context)

def unfollow_action(request, id):
    context = {}
    followee = User.objects.get(id=id)
    followee_profile = Profile.objects.filter(user_id=id).last()
    try:
        request_user_profile = Profile.objects.filter(user=request.user).last()
    except:
        request_user_profile = None

    request_user_profile.followers.remove(followee)
    request_user_profile.save()
    follower = request_user_profile.followers.all()

    followee_profile = Profile.objects.filter(user_id=id).last()
    context = {'user_profile': request_user_profile, 'followee_profile': followee_profile, 'followers': follower}

    return render(request, "socialnetwork/follower.html", context)


def followStream_action(request):

    errors = []
    context = {}
    followers_posts=[]
    request_user_profile = Profile.objects.filter(user = request.user).last()
    followers = request_user_profile.followers.all()

    posts=Post.objects.all().order_by('-time', 'id')
    for post in posts:
        if post.user in followers:
            followers_posts.append(post)

    context['posts'] = followers_posts

    return render(request, "socialnetwork/followerstream.html", context)


