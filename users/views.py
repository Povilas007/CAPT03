from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from newapp.models import Post
from django.contrib.auth.decorators import login_required
from users.forms import PostForm, UserRegisterForm
from django.http import Http404
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile_update.html', context)

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {'user': user, 'posts': posts}
    return render(request, 'profile.html', context)

@login_required
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        print(post)  # add this line to check if the post with the given ID exists
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    return render(request, 'delete_post.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a new Profile object for the newly registered user
            profile = Profile.objects.create(user=user)
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Your account has been created! You are now logged in as {username}')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out. See you soon!')
    return redirect('home')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # create a new post
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'tweet.html', {'form': form})


@login_required
def view_profile(request):
    return render(request, 'profile.html')

