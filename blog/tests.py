from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user_test')
        cls.post = Post.objects.create(
            title='Post_test',
            text='description of Post Test',
            status=Post.STATUS_CHOICES[0][0],
            author=user,
            url='urltest1',
        )
        cls.post_drf = Post.objects.create(
            title='Post_test_darft',
            text='description of Post Test draft',
            status=Post.STATUS_CHOICES[1][0],
            author=user,
            url='urltest2',
        )

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, 'Post_test')

    def test_post_detail(self):
        response = self.client.get(f'/blog/{self.post.url}/')
        self.assertEqual(response, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post.url]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        response = self.client.get(f'/blog/{self.post.url}/')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.text)

    def test_404(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_posts(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, self.post_drf.title)
