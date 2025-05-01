from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def announcements_list(request):
    user_filter = request.GET.get('user')  # e.g. ?user=2

    if user_filter and user_filter.isdigit():
        announcements = Announcement.objects.filter(author_id=user_filter)
    else:
        announcements = Announcement.objects.all()

    users = User.objects.filter(announcement__isnull=False).distinct()

    return render(request, 'announcements/list.html', {
        'announcements': announcements,
        'users': users,
        'selected_user_id': int(user_filter) if user_filter and user_filter.isdigit() else None,
    })

@login_required
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create.html', {'form': form})

@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, author=request.user)
    form = AnnouncementForm(request.POST or None, instance=announcement)
    if form.is_valid():
        form.save()
        messages.success(request, "Announcement updated.")
        return redirect('announcements_list')
    return render(request, 'announcements/edit.html', {'form': form})

@login_required
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, author=request.user)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, "Announcement deleted.")  # 👈 This triggers alert-danger
        return redirect('announcements_list')
    return render(request, 'announcements/confirm_delete.html', {'announcement': announcement})