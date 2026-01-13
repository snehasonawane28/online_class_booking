from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    # Auth
    path('login/', LoginAPI.as_view(), name='login'),
    path('register/', RegisterAPI.as_view(), name='register'),

    # Teacher
    path('teacher/availability/', TeacherAvailabilityAPI.as_view(), name='teacher-availability'),
    path('teacher/bookings/', TeacherBookingsAPI.as_view(), name='teacher-bookings'),

    # Student
    path('slots/', AvailableSlotsAPI.as_view(), name='available-slots'),
    path('book/', BookClassAPI.as_view(), name='book-class'),
]