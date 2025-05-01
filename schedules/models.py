from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WorkSchedule(models.Model):
    class EventType(models.TextChoices):
        WORK = 'Work', 'Work'
        SCHOOL = 'School', 'School'
        DRILL = 'Drill', 'Drill'
        OTHER = 'Other', 'Other'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=10, choices=EventType.choices, default=EventType.WORK)
    
    start_date = models.DateField()
    end_date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.event_type} from {self.start_date} {self.start_time} to {self.end_date} {self.end_time}"
