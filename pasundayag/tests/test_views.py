from importlib import import_module
from unittest import skip

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from pasundayag.models import IPCR, Rank
from pasundayag.views import ipcr_all


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        User.objects.create(username="admin")
        Rank.objects.create(name="django", slug="django")
        IPCR.objects.create(
            rank_id=1,
            title="django beginners",
            created_by_id=1,
            slug="django-beginners",
            price="20.00",
            image="django",
        )

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get("/", HTTP_HOST="noaddress.com")
        self.assertEqual(response.status_code, 400)
        response = self.c.get("/", HTTP_HOST="yourdomain.com")
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_ipcr_list_url(self):
        """
        Test rank response status
        """
        response = self.c.get(reverse("pasundayag:rank_list", args=["django"]))
        self.assertEqual(response.status_code, 200)

    def test_ipcr_detail_url(self):
        """
        Test items response status
        """
        response = self.c.get(reverse("pasundayag:ipcr_detail", args=["django-beginners"]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionPasundayag()
        response = ipcr_all(request)
        html = response.content.decode("utf8")
        self.assertIn("<title>BookPasundayag</title>", html)
        self.assertTrue(html.startswith("\n<!DOCTYPE html>\n"))
        self.assertEqual(response.status_code, 200)
