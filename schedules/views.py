from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from .forms import *
from .models import WorkSchedule
import json

def get_event_color(event_type):
    return {
        'Work': '#0d6efd',   # Bootstrap primary blue
        'Drill': '#198754', # Bootstrap success green
        'School': '#FFD700',
        'Other': '#6c757d',  # Bootstrap secondary gray
    }.get(event_type, '#6c757d')  # Default to gray

@login_required
def home(request):
    schedules = WorkSchedule.objects.all()
    event_data = [
    {
        'id': event.id,
        'title': f"{event.user.first_name or event.user.username}",
        'start': f"{event.start_date}T{event.start_time}",
        'end': f"{event.end_date}T{event.end_time}",
        'color': get_event_color(event.event_type),
    }
    for event in schedules
]
    return render(request, 'schedules/home.html', {
        'event_data_json': json.dumps(event_data, cls=DjangoJSONEncoder)
    })

@login_required
def add_schedule(request):
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            return redirect('home')
    else:
        form = WorkScheduleForm()
    return render(request, 'schedules/add_schedule.html', {'form': form})

@login_required
def delete_schedule(request, event_id):
    schedule = get_object_or_404(WorkSchedule, id=event_id, user=request.user)
    schedule.delete()
    return JsonResponse({'status': 'success'})

@login_required
def edit_schedule(request, event_id):
    schedule = get_object_or_404(WorkSchedule, id=event_id, user=request.user)
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule updated successfully!')
            return redirect('home')
    else:
        form = WorkScheduleForm(instance=schedule)
    return render(request, 'schedules/edit_schedule.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})