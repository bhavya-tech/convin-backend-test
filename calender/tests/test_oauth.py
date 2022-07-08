from django.test import TestCase
from urllib.parse import urlparse

class TestOauth(TestCase):
    
    def test_redirect_chain(self):
        response = self.client.get("/rest/v1/calendar/init/", follow=True)
        url_parse_result = urlparse(response.redirect_chain[0][0])

        self.assertEqual(url_parse_result.netloc, "accounts.google.com")
        self.assertEqual(url_parse_result.scheme, "https")
        self.assertEqual(url_parse_result.path, "/o/oauth2/auth")
        
        