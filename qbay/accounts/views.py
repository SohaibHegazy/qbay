from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from quizzes.models import Quiz
from django.contrib.auth.views import LogoutView

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def about(request):
    return render(request, 'accounts/about.html')

@login_required
def profile(request):
    user = request.user
    my_quizzes = Quiz.objects.filter(created_by=user, is_published=True)

    return render(request, 'profile.html', {
        'user': user,
        'my_quizzes': my_quizzes,
        'user_quizzes_created': my_quizzes,
    })


