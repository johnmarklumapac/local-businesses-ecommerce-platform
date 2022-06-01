from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestCartView(TestCase):
    def setUp(self):
        User.objects.create(username="admin")
        Category.objects.create(name="django", slug="django")
        Product.objects.create(
            category_id=1,
            title="django beginners",
            created_by_id=1,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        Product.objects.create(
            category_id=1,
            title="django intermediate",
            created_by_id=1,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        Product.objects.create(
            category_id=1,
            title="django advanced",
            created_by_id=1,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        self.client.post(reverse("cart:cart_add"), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(reverse("cart:cart_add"), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    def test_cart_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse("cart:cart_summary"))
        self.assertEqual(response.status_code, 200)

    def test_cart_add(self):
        """
        Test adding items to the cart
        """
        response = self.client.post(
            reverse("cart:cart_add"), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"qty": 4})
        response = self.client.post(
            reverse("cart:cart_add"), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"qty": 3})

    def test_cart_delete(self):
        """
        Test deleting items from the cart
        """
        response = self.client.post(reverse("cart:cart_delete"), {"productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {"qty": 1, "subtotal": "20.00"})

    def test_cart_update(self):
        """
        Test updating items from the cart
        """
        response = self.client.post(
            reverse("cart:cart_update"), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"qty": 2, "subtotal": "40.00"})
