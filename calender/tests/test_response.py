from django.test import TestCase

class TestResponse(TestCase):
    
    def test_invalid_response(self):
        response = self.client.get("/rest/v1/calendar/redirect/", secure=True)
        self.assertEqual(response.status_code, 400)