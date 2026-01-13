from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date, timedelta


class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    first_name = models.CharField(max_length=255, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=255, null=True, blank=True, default=None)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, null=True, blank=True, default=None)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    age = models.IntegerField(max_length=50, null=True, blank=True, default=None)
    subject = models.CharField(max_length=100, null=True, blank=True, default=None)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.username}"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.email} - {self.subject}"
    
class TeacherAvailability(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        if self.date != date.today() + timedelta(days=1):
            raise ValueError("Availability must be set for next day only")
        super().save(*args, **kwargs)

class ClassBooking(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active_student = models.BooleanField(default=True)

    class Meta:
        unique_together = ('teacher', 'date', 'start_time')