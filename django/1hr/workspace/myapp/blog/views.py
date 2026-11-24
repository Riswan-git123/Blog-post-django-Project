from pyexpat.errors import messages

from django.core.mail import send_mail
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post, AboutUs
from django.core.paginator import Paginator
from .forms import ContactForm, ForgotPasswordForm, LoginForm, RegisterForm, ResetPasswordForm, PostForm
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages




# static datas
# posts=[
#         {'id':1,"title":"post1","content":"content of post 1"},
#         {'id':2,"title":"post2","content":"content of post 2"},
#         {'id':3,"title":"post3","content":"content of post 3"},
#         {'id':4,"title":"post4","content":"content of post 4"},
#     ]


def index(request):
    blog_title="Latest posts by riswan"
    all_posts=Post.objects.filter(is_published=True)
    paginator= Paginator(all_posts, 5)
    page_number= request.GET.get("page")
    page_obj= paginator.get_page(page_number)
    return render(request,"blogs/index.html",{'blog_title':blog_title, 'page_obj':page_obj})

    
def detail(request,slug):
    # static
    # log=next((item for item in posts if item['id']==int(post)), None)a
    # logger=logging.getLogger("TESTING")
    #  logger.debug(f'log variable is {log}')
    post=get_object_or_404(Post, slug=slug)
    if not post.is_published and post.author != request.user:
        return redirect('blog:index')
    related_posts=Post.objects.filter(Category=post.Category, is_published=True).exclude(pk=post.id)
    return render(request,"blogs/base.html",{"post":post, 'related_posts':related_posts})


def home(request):
    return redirect(reverse('blog:riswan'))


def about(request):
    return HttpResponse("your in new url page,welcome")

def contact_view(request):
    if request.method == 'POST':
        form=ContactForm(request.POST)
        logger=logging.getLogger("TESTING")
        name = request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        if form.is_valid():
            
            logger.debug(f'post data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
        else:
             logger.debug('post data is failure give correct Deatails')
             return render(request,'blogs/contact.html',{'form':form,'name':name,'email':email,'message':message})
    return render(request,'blogs/contact.html')


def about_view(request):
    about_content=AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content="about content is none type"
    else:
        about_content=about_content.content

    return render(request,'blogs/about.html',{'about_content':about_content})

def register(request):
    form=RegisterForm()
    if request.method == 'POST':
        form=RegisterForm(request.POST)   
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            print('register succesful')
            user.save()
            return redirect('blog:login')         
    return render(request,'blogs/register.html',{'form':form})



def login(request):
    form=LoginForm()
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user=authenticate(username=username,password=password)
           
            if user is not None:
                auth_login(request,user)
                
                print("login success")
                return redirect("blog:dashboard")
    return render(request,'blogs/login.html',{'form':form})

@login_required(login_url='blog:login')
def dashboard(request):
    blog_title = "My Posts"
    posts = Post.objects.filter(author=request.user).order_by('-ceated_at')
    return render(request, 'blogs/dashboard.html', {
        'blog_title': blog_title,
        'posts': posts,
        'show_post_form': False,
        'editing_post': None,
    })


@login_required(login_url='blog:login')
def new_post(request):
    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.is_published = False
            post.save()
            messages.success(request, 'Your post was saved as a draft.')
            return redirect('blog:dashboard')

    return render(request, 'blogs/dashboard.html', {
        'blog_title': 'Create a Post',
        'posts': Post.objects.none(),
        'show_post_form': True,
        'post_form': post_form,
        'editing_post': None,
    })


@login_required(login_url='blog:login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Your post was updated.')
            return redirect('blog:dashboard')
    else:
        post_form = PostForm(instance=post)

    posts = Post.objects.filter(author=request.user).order_by('-ceated_at')
    return render(request, 'blogs/dashboard.html', {
        'blog_title': 'Edit Post',
        'posts': posts,
        'show_post_form': True,
        'post_form': post_form,
        'editing_post': post,
    })


@login_required(login_url='blog:login')
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Your post was deleted.')
    return redirect('blog:dashboard')


@login_required(login_url='blog:login')
@require_POST
def toggle_post_published(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    post.is_published = not post.is_published
    post.save()
    messages.success(request, 'Post published.' if post.is_published else 'Post moved to drafts.')
    return redirect('blog:dashboard')


def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    if request.method=='POST':
        form=ForgotPasswordForm(request.POST)

        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email) #gives all email values in auth_user table 
            
            token=default_token_generator.make_token(user) #expext user object,not string-->user.username
            uid=urlsafe_base64_encode(force_bytes(user.pk)) #create uid by user table primary key-->user table id
            current_site=get_current_site(request)
            domain=current_site.domain

            subject="reset password  requested"
            message=render_to_string('blogs/reset_password_email.html',{'domain':domain,'uid':uid,'token':token})
            send_mail(subject,message,"noreply@jvlcode.com",[email])
            # messages.success(request,"email has been sent")
            
    return render(request,'blogs/forgot_password.html')


def reset_password(request,uidb64,token):
    form=ResetPasswordForm()
    
    if request.method=='POST':
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,'your password has been reset succesfully')
                return redirect('blog:login')
            else:
                messages.error(request,'reset link is invalid')
                

        
    return render(request,'blogs/reset_password.html')
    


 
