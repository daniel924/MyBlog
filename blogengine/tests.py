from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post, Category, Tag

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

import markdown


def CreateTag():
  # Create the tag
  tag = Tag()
  tag.name = 'python'
  tag.description = 'The Python programming language'
  tag.save()
  return tag

def CreateCategory():
  category = Category()
  category.name = 'Robots'
  category.description = 'All about robots'
  category.save()
  return category
    
class PostTest(TestCase):

  def test_create_post(self):
    category = CreateCategory()
    tag = CreateTag()

    post = Post()
    post.title = 'My first post'
    post.text = 'This is my first blog post'
    post.pub_date = timezone.now()
    post.category = category
    post.save()
    post.tags.add(tag)
    post.save()

    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)
    only_post = all_posts[0]
    self.assertEquals(only_post, post)

    self.assertEquals(only_post, post)
    self.assertEquals(only_post.title, 'My first post')
    self.assertEquals(only_post.text, 'This is my first blog post')
    self.assertEquals(only_post.pub_date.day, post.pub_date.day)
    self.assertEquals(only_post.pub_date.month, post.pub_date.month)
    self.assertEquals(only_post.pub_date.year, post.pub_date.year)
    self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
    self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
    self.assertEquals(only_post.pub_date.second, post.pub_date.second)
    self.assertEquals(only_post.category.name, 'Robots')


class BaseAcceptenceTest(LiveServerTestCase):
  def setUp(self):
    self.client = Client()


class TagTest(TestCase):
  def test_create_tag(self):
    # Create the tag
    tag = Tag()
    # Add attributes
    tag.name = 'python'
    tag.description = 'The Python programming language'
    # Save it
    tag.save()
    # Check we can find it
    all_tags = Tag.objects.all()
    self.assertEquals(len(all_tags), 1)
    only_tag = all_tags[0]
    self.assertEquals(only_tag, tag)
    # Check attributes
    self.assertEquals(only_tag.name, 'python')
    self.assertEquals(only_tag.description, 'The Python programming language')


class AdminTest(BaseAcceptenceTest):
  fixtures = ['users.json']

  def setUp(self):
    self.client = Client()

  def Login(self):
    self.client.login(username='ali', password='alikat')

  def test_login(self):
    response = self.client.get('/admin/')

    self.assertEquals(response.status_code, 200)
    self.assertTrue('Log in' in response.content)
    
    self.client.login(username='ali', password='alikat')
    response = self.client.get('/admin/')
    self.assertEquals(response.status_code, 200)
    self.assertTrue('Log out' in response.content)

  def test_create_category(self):
    self.Login()

    # Check response
    response = self.client.get('/admin/blogengine/category/add/')
    self.assertEquals(response.status_code, 200)

    response = self.client.post('/admin/blogengine/category/add/', {
        'name': 'Robots',
        'description': 'All about robots'
        },
        follow=True
    )
    self.assertEquals(response.status_code, 200)
    self.assertTrue('added successfully' in response.content)

    all_categories = Category.objects.all()
    self.assertEquals(len(all_categories), 1)

  def test_create_post(self):
    CreateCategory()
    tag = CreateTag()

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
            'pub_date_1': '22:00:00',
            'category': '1',
            'slug': 'my-first-post',
            'tags': '1'},
        follow=True)

    self.assertEquals(response.status_code, 200)
    self.assertTrue('added successfully' in response.content)

    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)

  def test_edit_category(self):
    CreateCategory()
    self.Login()

    response = self.client.post('/admin/blogengine/category/1/', {
        'name': 'Kitties',
        'description': 'All about kitties'
        }, follow=True)
    
    self.assertTrue(response.status_code, 200)
    self.assertTrue('changed successfully' in response.content)
    all_categories = Category.objects.all()
    self.assertEquals(len(all_categories), 1)
    only_category = all_categories[0]
    self.assertEquals(only_category.name, 'Kitties')

  def test_delete_category(self):
    CreateCategory()
    self.Login()

    response = self.client.post('/admin/blogengine/category/1/delete/', {
        'post': 'yes'
      }, follow=True)
    self.assertEquals(response.status_code, 200)
    self.assertTrue('deleted successfully' in response.content)
    all_categories = Category.objects.all()
    self.assertEquals(len(all_categories), 0)

  def test_edit_post(self):
    CreateCategory()
    tag = CreateTag()

    post = Post()
    post.title = 'My first post'
    post.text = 'Hello World'
    post.pub_date = timezone.now()
    post.save()
    post.tags.add(tag)
    post.save()

    self.client.login(username='ali', password='alikat')

    # Edit the post
    response = self.client.post(
        '/admin/blogengine/post/1/', {
            'title': 'My second post',
            'text': 'Hello world part 2',
            'pub_date_0': '2014-07-12',
            'pub_date_1': '22:00:00',
            'category': '1',
            'tags': '1'},
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
    CreateCategory()
    tag = CreateTag()

    post = Post()
    post.title = 'My first post'
    post.text = 'Hello World'
    post.pub_date = timezone.now()
    post.save()
    post.tags.add(tag)
    post.save()
    
    self.Login()

    # Delete the post
    response = self.client.post(
        '/admin/blogengine/post/1/delete/',
        {'post': 'yes'}, follow=True)
    self.assertEquals(response.status_code, 200)
    
    self.assertTrue('deleted successfully' in response.content)
    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 0)

  def test_create_tag(self):
    # Log in
    self.Login()
    # Check response code
    response = self.client.get('/admin/blogengine/tag/add/')
    self.assertEquals(response.status_code, 200)
    # Create the new tag
    response = self.client.post('/admin/blogengine/tag/add/', {
        'name': 'python',
        'description': 'The Python programming language'
        },
        follow=True
        )
    self.assertEquals(response.status_code, 200)
    # Check added successfully
    self.assertTrue('added successfully' in response.content)
    # Check new tag now in database
    all_tags = Tag.objects.all()
    self.assertEquals(len(all_tags), 1)

  def test_edit_tag(self):
    # Create the tag
    tag = Tag()
    tag.name = 'python'
    tag.description = 'The Python programming language'
    tag.save()
    # Log in
    self.Login()
    # Edit the tag
    response = self.client.post('/admin/blogengine/tag/1/', {
      'name': 'perl',
      'description': 'The Perl programming language'
      }, follow=True)
    self.assertEquals(response.status_code, 200)
    # Check changed successfully
    self.assertTrue('changed successfully' in response.content)
    # Check tag amended
    all_tags = Tag.objects.all()
    self.assertEquals(len(all_tags), 1)
    only_tag = all_tags[0]
    self.assertEquals(only_tag.name, 'perl')
    self.assertEquals(only_tag.description, 'The Perl programming language')

  def test_delete_tag(self):
    # Create the tag
    tag = Tag()
    tag.name = 'python'
    tag.description = 'The Python programming language'
    tag.save()
    # Log in
    self.Login()
    # Delete the tag
    response = self.client.post('/admin/blogengine/tag/1/delete/', {
        'post': 'yes'
        }, follow=True)
    self.assertEquals(response.status_code, 200)

    # Check deleted successfully
    self.assertTrue('deleted successfully' in response.content)

    # Check tag deleted
    all_tags = Tag.objects.all()
    self.assertEquals(len(all_tags), 0)


class PostViewTest(BaseAcceptenceTest):
  def setUp(self):
    self.client = Client()

  def test_index(self):
    category = CreateCategory()
    
    post = Post()
    post.title = 'My first post'
    post.text = 'Hello [World](http://127.0.0.1:8000/)'
    post.pub_date = timezone.now()
    post.category = category
    post.save()

    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)

    response = self.client.get('/')
    self.assertEquals(response.status_code, 200)

    self.assertTrue(post.title in response.content)
    self.assertTrue(markdown.markdown(post.text) in response.content)

    self.assertTrue(str(post.pub_date.year) in response.content)
    self.assertTrue(post.pub_date.strftime('%b') in response.content)
    self.assertTrue(str(post.pub_date.day) in response.content)
    self.assertTrue('<a href="http://127.0.0.1:8000/">World</a>' in response.content)

  def test_post_page(self):
    # Create the category
    category = Category()
    category.name = 'python'
    category.description = 'The Python programming language'
    category.save()
    
    post = Post()
    post.title = 'My first post'
    post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
    post.slug = 'my-first-post'
    post.pub_date = timezone.now()
    post.category = category
    post.save()
  
    # Check new post saved
    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)
    only_post = all_posts[0]
    self.assertEquals(only_post, post)
  
    # Get the post URL
    post_url = only_post.get_absolute_url()
    # Fetch the post
    response = self.client.get(post_url)
    self.assertEquals(response.status_code, 200)
    # Check the post title is in the response
    self.assertTrue(post.title in response.content)
    # Check the post category is in the response
    self.assertTrue(post.category.name in response.content)
    # Check the post text is in the response
    self.assertTrue(markdown.markdown(post.text) in response.content)
    # Check the post date is in the response
    self.assertTrue(str(post.pub_date.year) in response.content)
    self.assertTrue(post.pub_date.strftime('%b') in response.content)
    self.assertTrue(str(post.pub_date.day) in response.content)
    # Check the link is marked up properly
    self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

  def test_category_page(self):
    # Create the category
    category = Category()
    category.name = 'python'
    category.description = 'The Python programming language'
    category.save()
  
    # Create the post
    post = Post()
    post.title = 'My first post'
    post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
    post.slug = 'my-first-post'
    post.pub_date = timezone.now()
    post.category = category
    post.save()
    # Check new post saved
    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)
    only_post = all_posts[0]
    self.assertEquals(only_post, post)
    # Get the category URL
    category_url = post.category.get_absolute_url()
    # Fetch the category
    response = self.client.get(category_url)
    self.assertEquals(response.status_code, 200)
    # Check the category name is in the response
    self.assertTrue(post.category.name in response.content)
   
    # Check the post text is in the response
    self.assertTrue(markdown.markdown(post.text) in response.content)
    # Check the post date is in the response
    self.assertTrue(str(post.pub_date.year) in response.content)
    self.assertTrue(post.pub_date.strftime('%b') in response.content)
    self.assertTrue(str(post.pub_date.day) in response.content)
    # Check the link is marked up properly
    self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)


  def test_tag_page(self):
    # Create the tag
    tag = CreateTag()
    # Create the post
    post = Post()
    post.title = 'My first post'
    post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
    post.slug = 'my-first-post'
    post.pub_date = timezone.now()
    post.save()
    post.tags.add(tag)
    post.save()

    # Check new post saved
    all_posts = Post.objects.all()
    self.assertEquals(len(all_posts), 1)
    only_post = all_posts[0]
    self.assertEquals(only_post, post)
    # Get the tag URL
    tag_url = post.tags.all()[0].get_absolute_url()
    # Fetch the tag
    response = self.client.get(tag_url)
    self.assertEquals(response.status_code, 200)
                                                                                                                                        # Check the tag name is in the response
    self.assertTrue(post.tags.all()[0].name in response.content)

    # Check the post text is in the response
    self.assertTrue(markdown.markdown(post.text) in response.content)

    # Check the post date is in the response
    self.assertTrue(str(post.pub_date.year) in response.content)
    self.assertTrue(post.pub_date.strftime('%b') in response.content)
    self.assertTrue(str(post.pub_date.day) in response.content)
    # Check the link is marked up properly
    self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

class FlatPageViewTest(BaseAcceptenceTest):
    def test_create_flat_page(self):
      # Create flat page
      page = FlatPage()
      page.url = '/about/'
      page.title = 'About me'
      page.content = 'All about me'
      page.save()

      # Add the site
      page.sites.add(Site.objects.all()[0])
      page.save()
      # Check new page saved
      all_pages = FlatPage.objects.all()
      self.assertEquals(len(all_pages), 1)
      only_page = all_pages[0]
      self.assertEquals(only_page, page)

      # Check data correct
      self.assertEquals(only_page.url, '/about/')
      self.assertEquals(only_page.title, 'About me')
      self.assertEquals(only_page.content, 'All about me')
      
      # Get URL
      page_url = only_page.get_absolute_url()

      # Get the page
      response = self.client.get(page_url)
      self.assertEquals(response.status_code, 200)

      # Check title and content in response
      self.assertTrue('About me' in response.content)
      self.assertTrue('All about me' in response.content)
