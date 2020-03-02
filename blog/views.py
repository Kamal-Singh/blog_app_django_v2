from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Blog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import UserSignupForm,CreateBlogForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponse('User Created Successfully!!')
        else:
            return HttpResponse('Invalid Credentials!!')
    form = UserSignupForm()
    context = {'form': form}
    return render(request,'user/signup.html',context)

def user_signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            next_page = request.GET.get('next','')
            if next_page:
                return HttpResponseRedirect(next_page)
            return HttpResponse("User Signed In Successfully!!")
        else:
            return HttpResponse("Invalid Credentials!!")
    elif request.user.is_authenticated:
        return HttpResponse("You are already logged in!!")
    context = {}
    return render(request,'user/signin.html',context)

def user_logout(request):
    if request.user.is_authenticated == False:
        return HttpResponse("You are already Logged Out!!")
    logout(request)
    return HttpResponseRedirect(reverse('blog:user_signin'))

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST)
        print(form)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return HttpResponse('New Blog Created!!')
        else:
            context = {'form': form}
            return render(request,'blog/create_blog.html',context)
    form = CreateBlogForm()
    context = {'form': form}
    return render(request,'blog/create_blog.html',context)