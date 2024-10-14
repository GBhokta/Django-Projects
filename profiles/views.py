from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def view_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    
    # Handle the profile picture URL
    profile_picture_url = profile.profile_picture.url if profile.profile_picture else None

    return render(request, 'profiles/profile_view.html', {
        'profile': profile,
        'profile_picture_url': profile_picture_url,
    })

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:view_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})
