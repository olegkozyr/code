from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post


# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.title = 'A good title'
        cls.body = 'Nice body content'
        cls.username = 'testuser'
        cls.url = '/post/1/'
        cls.redirect_code = 302

        cls.user = get_user_model().objects.create_user(
            username=cls.username,
            email='test@emain.com',
            password='secret'
        )

        cls.post = Post.objects.create(
            title=cls.title,
            body=cls.body,
            author=cls.user
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, self.title)
        self.assertEqual(self.post.body, self.body)
        self.assertEqual(self.post.author.username, self.username)
        self.assertEqual(str(self.post), self.title)
        self.assertEqual(self.post.get_absolute_url(), self.url)

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.body)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detailview(self):
        response = self.client.get(reverse('post_detail',
                                   kwargs={'pk': self.post.pk}))
        no_response = self.client.get(self.url.replace('1', '100000'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, self.title)
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_createview(self):
        title = 'New title'
        body = 'New text'
        response = self.client.post(
            reverse('post_new'),
            {
                'title': title,
                'body': body,
                'author': self.user.id,
            },
        )
        self.assertEqual(response.status_code, self.redirect_code)
        self.assertEqual(Post.objects.last().title, title)
        self.assertEqual(Post.objects.last().body, body)

    def test_post_updateview(self):
        title = 'Updated title'
        body = 'Updated text'
        response = self.client.post(
            reverse('post_edit', args='1'),
            {
                'title': title,
                'body': body,
            },
        )
        self.assertEqual(response.status_code, self.redirect_code)
        self.assertEqual(Post.objects.last().title, title)
        self.assertEqual(Post.objects.last().body, body)

    def test_post_deleteview(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, self.redirect_code)
