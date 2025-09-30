from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from .models import Post


class PostTests(TestCase):
    _text = 'This is a test!'

    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(text=PostTests._text)

    def test_model_content(self):
        self.assertEqual(self.post.text, PostTests._text)

    def test_url_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_ulr_available_by_name(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 201)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, PostTests._text)
