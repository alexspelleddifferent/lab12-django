from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower

# Create your views here.
def home(request):
    app_name = 'Synthwave Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):
    # function tries to add new video to database. first it checks if the link is valid, gives different error messages
    # based on reason why it might not be valid
    if request.method == 'POST':
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                return redirect('video_list')
            except ValidationError:
                messages.warning(request, 'Invalid Youtube URL')
            except IntegrityError:
                messages.warning(request, 'You already added that video')

        messages.warning(request, 'Check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})
        
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

def video_list(request):

    search_form = SearchForm(request.GET)
    # renders the video list, but first provides a field for user to enter a search term to search through the list of videos by
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))

    else:
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})

def video_details(request, video_pk):

    video = get_object_or_404(Video, pk=video_pk)

    return render(request, 'video_collection/video_details.html', {'video': video})
