from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth import logout

def home(request):
    return render(request, 'home.html')

def feed(request):
    posts = Post.objects.all().order_by('-created_at')  
    return render(request, 'feed.html', {'posts': posts})

def login_view(request):
    next_url = request.GET.get('next', 'upload_post')  # fallback to upload_post
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html', {'next': next_url})

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            User.objects.create_user(username=username, email=email, password=password1)
            return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')

@login_required
def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'upload_post.html', {'form': form})


@login_required
def upload_photo(request):
    if request.method == 'POST':
        # Handle form submission here (image and comment upload logic)
        pass
    return render(request, 'upload.html')

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    
    # Check if the user has already liked the post
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)  # Remove like
        post.likes -= 1  # Decrease like count
    else:
        post.liked_by.add(request.user)  # Add like
        post.likes += 1  # Increase like count

    post.update_like_count()  # Update the like count in the database
    return redirect('feed')  # Redirect to the feed after like action


def logout_view(request):
    logout(request)
    return render(request, 'thank_you.html') 