from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer
from datetime import date, datetime, timedelta


# Create your views here.
class LoginAPI(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    # permission_classes = [IsAuthenticated]

    # def post(self, request):

    #     data = request.data

    #     try:
    #         user = User.objects.get(email=data['email'])
    #     except User.DoesNotExist:
    #         return Response(
    #             {"error": "Invalid email or password"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if not user.check_password(data['password']):
    #         return Response(
    #             {"error": "Invalid password"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     data = {
    #         "id": user.id,
    #         "email": user.email,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "role": user.role,
    #     }

    #     return Response(
    #         {
    #             "message": "Login successful",
    #             "data": data
    #          },
    #         status=status.HTTP_200_OK
    #     )

class RegisterAPI(APIView):
    permission_classes = []  # Public

    def post(self, request):
        data = request.data

        if User.objects.filter(email=data['email']).exists():
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=data['email'],   # IMPORTANT
            email=data['email'],
            password=data['password'],  # NO make_password
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            age=data['age'],
            role=data['role'],
        )

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            },
            status=status.HTTP_201_CREATED
        )
    
class TeacherAvailabilityAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'teacher':
            return Response({"error": "Only teachers allowed"}, status=403)

        data = request.data
        next_day = date.today() + timedelta(days=1)

        availability = TeacherAvailability.objects.create(
            teacher=request.user,
            date=next_day,
            start_time=data['start_time'],
            end_time=data['end_time']
        )

        return Response({"message": "Availability added"})

class AvailableSlotsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        slots = []

        for avail in TeacherAvailability.objects.all():
            start = datetime.combine(avail.date, avail.start_time)
            end = datetime.combine(avail.date, avail.end_time)

            while start + timedelta(hours=1) <= end:
                slots.append({
                    "teacher": avail.teacher.email,
                    "subject": avail.teacher.teacherprofile.subject,
                    "start_time": start.time(),
                    "end_time": (start + timedelta(hours=1)).time()
                })
                start += timedelta(hours=1)

        return Response(slots)

class BookClassAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students allowed"}, status=403)

        data = request.data

        booking = ClassBooking.objects.create(
            teacher_id=data['teacher_id'],
            student=request.user,
            date=data['date'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            is_active_student=True
        )

        return Response({"message": "Class booked"})

class TeacherBookingsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'teacher':
            return Response({"error": "Only teachers allowed"}, status=403)

        bookings = ClassBooking.objects.filter(teacher=request.user)

        return Response([
            {
                "student": b.student.email,
                "start_time": b.start_time,
                "end_time": b.end_time
            } for b in bookings
        ])