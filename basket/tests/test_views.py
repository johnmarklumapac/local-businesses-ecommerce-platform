from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from pasundayag.models import IPCR, Rank


class TestBasketView(TestCase):
    def setUp(self):
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
        IPCR.objects.create(
            rank_id=1,
            title="django intermediate",
            created_by_id=1,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        IPCR.objects.create(
            rank_id=1, title="django advanced", created_by_id=1, slug="django-beginners", price="20.00", image="django"
        )
        self.client.post(reverse("basket:basket_add"), {"ipcrid": 1, "ipcrqty": 1, "action": "post"}, xhr=True)
        self.client.post(reverse("basket:basket_add"), {"ipcrid": 2, "ipcrqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse("basket:basket_summary"))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse("basket:basket_add"), {"ipcrid": 3, "ipcrqty": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"qty": 4})
        response = self.client.post(
            reverse("basket:basket_add"), {"ipcrid": 2, "ipcrqty": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"qty": 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(reverse("basket:basket_delete"), {"ipcrid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {"qty": 1, "subtotal": "20.00"})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse("basket:basket_update"), {"ipcrid": 2, "ipcrqty": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"qty": 2, "subtotal": "40.00"})
