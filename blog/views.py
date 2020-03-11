from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Blog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import UserSignupForm,CreateBlogForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_signup(request):
    if request.user.is_authenticated:
        return HttpResponse("You are already signed in!!")
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
    if request.user.is_authenticated:
        return HttpResponse("You are already logged in!!")
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

@login_required
def edit_blog(request,blog_id):
    if request.method == 'POST':
        blog = Blog.objects.get(id=blog_id)
        form = CreateBlogForm(request.POST,instance=blog)
        if form.is_valid():
            post = form.save(commit=False)
            post.author =  request.user
            form.save(commit=True)
            return HttpResponse("Form Edited Successfully!!")
        else:
            return HttpResponse("Edit is Invalid!!")
    blog = Blog.objects.get(id = blog_id)
    if blog:
        if request.user != blog.author:
            return HttpResponse("You are not authorized to do this action!!")
        form = CreateBlogForm(instance = blog)
        context = {'form': form}
        return render(request,'blog/edit_blog.html',context)
    else:
        return HttpResponse("No such blog exists!!")

def view_blog(request,blog_id):
    blog = Blog.objects.filter(id=blog_id).first()
    print(blog)
    context = {'blog':blog}
    return render(request,'blog/view_blog.html',context)

def index(request):
    blogs = Blog.objects.all()
    if blogs.count() != 0:
        context = {'blogs': blogs}
    else:
        context = {}
    return render(request,'blog/index.html',context)

@login_required
def delete_blog(request,blog_id):
    blog = Blog.objects.get(id=blog_id)
    if blog:
        if request.user != blog.author:
            return HttpResponse("You are not authorized to do this action!!")
        blog.delete()
        return HttpResponse("Blog Deleted Successfully!!")
    else:
        return HttpResponse("No such Blog Exist!!")