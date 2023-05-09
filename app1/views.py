from django.shortcuts import render, redirect
import os
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from PIL import Image


from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from django.conf import settings



# Create your views here.
def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    posts = Post.objects.filter(
        Q(Author__username__icontains=q) |
        Q(title__icontains=q) |
        Q(body__icontains=q)
    )
    posts = posts.order_by('-time_created')
    paginator = Paginator(posts, 8) 

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {'posts': posts, 'page': page, 'page_range': paginator.page_range}

 
    return render(request, 'index.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            subject = 'Reset Password Request:'
            reset_link = request.build_absolute_uri('/') + f'reset_password/{uid}/{token}/'
            #message = render_to_string('reset_password.html', {'reset_link': reset_link})
            #message = 'just to try some sample message'
            message = f'Click on the link to reset your password: {reset_link}'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [email], fail_silently=False)
            messages.success(request, 'An email has been sent to reset your password')
            return redirect ('login')
        else:
            messages.error(request, 'No user found with that email address')
    return render(request, 'forgot_password.html')

def reset_password(request, uid, token):
    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    # messages.success(request, 'Password reset successful')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match')
            return render(request, 'reset_password.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    messages.error(request, 'Invalid or Expired link')
    return redirect('forgot_password')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['repeat_password']
         
        if password == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'E-mail already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,email = email, password  = password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not matched')
            return redirect('register')

    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']

         user = auth.authenticate(username = username, password  = password)

         if user is not None:
            auth.login(request, user)
            return redirect('index')
            #return render(request, 'index.html')l
         else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def postpage(request, pk):
   posts = Post.objects.get(id=pk)
   user = request.user
   context = {'user': user, 'posts':posts, 'one':1, 'two':2}
   return render(request, 'postpage.html', context)


from .models import Preference
@login_required
def postpreference(request, pk, userpreference):
        user = request.user
        pk = pk
        
        if request.method == "POST":
                posts = Post.objects.get(id=pk)

                obj=''

                valueobj=''

                try:
                        obj = Preference.objects.get(user= request.user, post = posts)

                        valueobj= obj.value #value of userpreference


                        valueobj= int(valueobj)

                        userpreference = int(userpreference)
                
                        if valueobj != userpreference:
                                obj.delete()


                                upref= Preference()
                                upref.user= request.user

                                upref.post= posts

                                upref.value= userpreference


                                if userpreference == 1 and valueobj != 1:
                                        posts.likes += 1
                                        posts.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        posts.dislikes += 1
                                        posts.likes -= 1
                                

                                upref.save()

                                posts.save()
                        
                        
                                context= {'posts': posts, 'user':user,
                                  'pk': pk}

                                return redirect ('postpage', pk = pk)

                        elif valueobj == userpreference:
                                obj.delete()
                        
                                if userpreference == 1:
                                        posts.likes -= 1
                                elif userpreference == 2:
                                        posts.dislikes -= 1

                                posts.save()

                                context= {'posts': posts, 'user':user,
                                  'pk': pk}

                                return redirect ('postpage', pk = pk)
                                
                        
        
                
                except Preference.DoesNotExist:
                        upref= Preference()

                        upref.user= request.user

                        upref.post= posts

                        upref.value= userpreference

                        userpreference= int(userpreference)

                        if userpreference == 1:
                                posts.likes += 1
                        elif userpreference == 2:
                                posts.dislikes +=1

                        upref.save()

                        posts.save()                            


                        context= {'posts': posts,'user':user,
                          'pk': pk}

                        return redirect ('postpage', pk = pk)


        else:
                posts = Post.objects.get(id = pk)
                context= {'posts': posts, 'user':user,
                          'pk': pk}

                return redirect ('postpage',pk= pk )





@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    current_user = request.user
    if request.method == 'POST':
        image_file = request.FILES.get('post-image')
        if image_file:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'post_images'))
            filename = fs.save(image_file.name, image_file)
            image_path = 'post_images/' + filename
        else:
            image_path = ''
        post = Post(                
             Author=current_user,
             title=request.POST.get('title'),
             category=request.POST.get('category'),
             body=request.POST.get('blog-body'),
             references=request.POST.get('references'),
             image=image_path
        )
        post.save()
        
        return redirect('index')

    context = {'form': form, 'blog_body': 'blog_body'}
    return render(request, 'create_post.html', context)


@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        image_file = request.FILES.get('post-image')
        if image_file:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'post_images'))
            filename = fs.save(image_file.name, image_file)
            image_path = 'post_images/' + filename
            if post.image:
                 old_image_path = os.path.join(settings.MEDIA_ROOT, post.image.name)
                 if os.path.exists(old_image_path):
                      os.remove(old_image_path)
        else:
            image_path = post.image

        form = PostForm(request.POST, instance=post)
        post.title =  request.POST.get('title')
        post.category =  request.POST.get('category')
        post.references =  request.POST.get('references')
        post.body =  request.POST.get('blog-body') 
        post.image = image_path

        post.save()   

        return redirect('postpage', pk=post.id)
    else:
        form = PostForm(instance=post)
    context =  {'form': form, 'post': post}
    return render(request, 'updatePost.html', context)

@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('index')
    #context = {"post": post}
    #return render(request, "postpage.html", context)



def about(request):
  #if statement here for user authentification
   return render(request, 'about.html')

def contact(request):
  #if statement here for user authentification
   return render(request, 'contact.html')

def page(request):
  #if statement here for user authentification
   return render(request, 'page.html')

def category(request, pk):
   posts = Post.objects.filter(category = pk).order_by('-time_created')
   paginator = Paginator(posts, 8) 

   page_number = request.GET.get('page', 1)
   page = paginator.get_page(page_number)
   context = {'posts': posts, 'page': page, 'page_range': paginator.page_range}
   return render(request, 'index.html', context)