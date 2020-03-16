from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Blog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import UserSignupForm,CreateBlogForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
# from django.utils import timezone

# Create your views here.
def generate_error_context(error_code='404',message1='The page',message2='was not found'):
    return {
            'error_code': error_code,
            'message1': message1,
            'message2': message2
    }
def user_signup(request):
    if request.user.is_authenticated:
        context = generate_error_context('403','you are','already logged in')
        return render(request,'error.html',context)
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'User Created Successfully!!')
        else:
            messages.error(request,"Invalid Credentials!!")
    form = UserSignupForm()
    context = {'form': form}
    return render(request,'user/signup.html',context)

def user_signin(request):
    if request.user.is_authenticated:
        context = generate_error_context('403','you are','already logged in')
        return render(request,'error.html',context)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            next_page = request.GET.get('next','')
            if next_page:
                return HttpResponseRedirect(next_page)
            messages.success(request,'User Loggedin Successfully!!')
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            messages.error(request,"Invalid Credentials!!")
    context = {}
    return render(request,'user/signin.html',context)

def user_logout(request):
    if request.user.is_authenticated == False:
        context = generate_error_context('403','You are','already logged out')
        return render(request,'error.html',context)
    logout(request)
    messages.success(request,'User Successfully Logged Out!!')
    return HttpResponseRedirect(reverse('blog:index'))

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST)
        print(form)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request,'Blog Created Successfully!!')
        else:
            context = {'form': form}
            messages.success(request,'Please Enter the correct Data!!')
            return render(request,'blog/create_blog.html',context)
    form = CreateBlogForm()
    context = {'form': form}
    return render(request,'blog/create_blog.html',context)

@login_required
def edit_blog(request,blog_id):
    if request.method == 'POST':
        blog = Blog.objects.get(id=blog_id)
        if request.user != blog.author:
            context = generate_error_context('403','you are not','authorized to do this action')
            return render(request,'error.html',context)
        form = CreateBlogForm(request.POST,instance=blog)
        if form.is_valid():
            post = form.save(commit=False)
            post.author =  request.user
            form.save(commit=True)
            messages.success(request,'Form Edited Successfully')
            return HttpResponseRedirect(reverse('blog:view_blog',kwargs={'blog_id': blog_id}))
        else:
            messages.success(request,'Edit is Invalid!!')
            context = {'form': form}
            return render(request,'blog/edit_blog.html',context)
    blog = Blog.objects.get(id = blog_id)
    if blog:
        if request.user != blog.author:
            context = generate_error_context('403','you are not','authorized to do this action')
            return render(request,'error.html',context)
        form = CreateBlogForm(instance = blog)
        context = {'form': form}
        return render(request,'blog/edit_blog.html',context)
    else:
        context = generate_error_context('500','no such','blog exists')
        return render(request,'error.html',context)

def view_blog(request,blog_id):
    blog = Blog.objects.filter(id=blog_id).first()
    if blog:
        # blog.date_created = blog.date_created.replace(tzinfo=timezone('IN'))
        context = {'blog':blog}
        return render(request,'blog/view_blog.html',context)
    context = generate_error_context('500','no such','blog exists')
    return render(request,'error.html',context)


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
            context = generate_error_context('403','you are not','authorized to do this action')
            return render(request,'error.html',context)
        blog.delete()
        messages.success(request,'Form Deleted Successfully')
        return HttpResponseRedirect(reverse('blog:index'))
    else:
        context = generate_error_context('500','no such','blog exists')
        return render(request,'error.html',context)

def handler404(request,*args,**kwargs):
    context = generate_error_context()
    return render(request,'error.html',context)

def handler500(request,*args,**kwargs):
    context = generate_error_context('500','Internal server Error','')
    return render(request,'error.html',context)