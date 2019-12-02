from django.test import TestCase, Client
from django.urls import  reverse, resolve
from django.contrib.auth.models import User

from blog.models import Blog, BlogType
from blog.views import blog_detail

class BlogDetailTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BlogDetailTest, cls).setUpClass()
        # 创建用户
        user = User.objects.create_user('test_blog_detail', email='test_blog_detail@user.com', password='test_blog_detail')
        # 创建博客分类
        blog_type = BlogType.objects.create(type_name='test')
        # 创建博客
        cls.blog = Blog.objects.create(title='test title', content='test content', author=user, blog_type=blog_type)

        cls.client = Client()
        # 访问新创建的博客
        cls.response = cls.client.get(reverse('blog:blog_detail', args=f'{cls.blog.pk}'))

    def test_blog_detail_url_resolve_view(self):
        view = resolve(f'/blog/blog_detail/{self.blog.pk}')
        self.assertEqual(view.func, blog_detail)

    def test_blog_detail_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        pass