from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post


class PostTest(TestCase):

  def test_create_post(self):
    post = Post()
    post.title = 'My first post'
    post.text = 'This is my first blog post'
    post.pub_date = timezone.now()
    post.save()

    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)
    only_post = all_posts[0]
    
    self.assertEquals(only_post, post)
    self.assertEquals(only_post.title, 'My first post')
    self.assertEquals(only_post.text, 'This is my first blog post')
    self.assertEquals(only_post.pub_date.day, post.pub_date.day)
    self.assertEquals(only_post.pub_date.month, post.pub_date.month)
    self.assertEquals(only_post.pub_date.year, post.pub_date.year)
    self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
    self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
    self.assertEquals(only_post.pub_date.second, post.pub_date.second)

class AdminTest(LiveServerTestCase):
  fixtures = ['users.json']

  def setUp(self):
    self.client = Client()

  def test_login(self):
    response = self.client.get('/admin/')

    self.assertEquals(response.status_code, 200)
    self.assertTrue('Log in' in response.content)
    
    self.client.login(username='ali', password='alikat')
    response = self.client.get('/admin/')
    self.assertEquals(response.status_code, 200)
    self.assertTrue('Log out' in response.content)

  def test_create_post(self):
    # Log in
    self.client.login(username='ali', password='alikat')

    # Check response
    response = self.client.get('/admin/blogengine/post/add/')
    self.assertEquals(response.status_code, 200)
    
    # Create new post
    response = self.client.post(
        '/admin/blogengine/post/add/', {
            'title': 'My first post',
            'text': 'Hello World',
            'pub_date_0': '2014-07-11',
            'pub_date_1': '22:00:00'},
        follow=True)

    self.assertEquals(response.status_code, 200)
    self.assertTrue('added successfully' in response.content)

    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)
  
  def test_edit_post(self):
    post = Post()
    post.title = 'My first post'
    post.text = 'Hello World'
    post.pub_date = timezone.now()
    post.save()

    self.client.login(username='ali', password='alikat')

    # Edit the post
    response = self.client.post(
        '/admin/blogengine/post/1/', {
            'title': 'My second post',
            'text': 'Hello world part 2',
            'pub_date_0': '2014-07-12',
            'pub_date_1': '22:00:00'},
        follow=True
    )
    self.assertEquals(response.status_code, 200)

    # Check changed successfully
    self.assertTrue('changed successfully' in response.content)

    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)
    only_post = all_posts[0]
    self.assertEquals(only_post.title, 'My second post')
    self.assertEqual(only_post.text, 'Hello world part 2')

  def test_delete_post(self):
    post = Post()
    post.title = 'My first post'
    post.text = 'Hello World'
    post.pub_date = timezone.now()
    post.save()
    
    self.client.login(username='ali', password='alikat')

    # Delete the post
    response = self.client.post(
        '/admin/blogengine/post/1/delete/',
        {'post': 'yes'}, follow=True)
    self.assertEquals(response.status_code, 200)
    
    self.assertTrue('deleted successfully' in response.content)
    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 0)

class PostViewTest(LiveServerTestCase):
  def setUp(self):
    self.client = Client()

  def test_index(self):
    post = Post()
    post.title = 'My first post'
    post.text = 'Hello World'
    post.pub_date = timezone.now()
    post.save()

    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)

    response = self.client.get('/')
    self.assertEquals(response.status_code, 200)

    self.assertTrue(post.title in response.content)
    self.assertTrue(post.text in response.content)

    self.assertTrue(str(post.pub_date.year) in response.content)
    self.assertTrue(post.pub_date.strftime('%b') in response.content)
    self.assertTrue(str(post.pub_date.day) in response.content)

