from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import Image

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to clear the form after a successful submission

    form = ImageForm()
    img = Image.objects.all()
    return render(request, 'view/home.html', {'form': form, 'img': img})
