from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

class BookingTest(APITestCase):

    def test_teacher_availability(self):
        response = self.client.post('/api/teacher/availability/', {
            "start_time": "11:00",
            "end_time": "18:00"
        })
        self.assertEqual(response.status_code, 201) 