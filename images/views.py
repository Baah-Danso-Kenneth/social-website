from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from images.forms import ImageCreationForm


def image_create(request):
    if request.method == 'POST':
        form = ImageCreationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()

            messages.success(request, 'Image was added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreationForm()

    context = {'form': form, 'section': 'images'}
    return render(request, 'images/create.html', context)

