from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import ListView, DetailView
from blogengine.models import Post, Category, Tag
from blogengine.views import CategoryListView, TagListView

admin.autodiscover()
urlpatterns = patterns('',
    # Index
    url('^$', ListView.as_view(
        model=Post,
        paginate_by=5,
        )),

     # Individual posts
     url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Post,
        )),

     # Categories
     url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(
       paginate_by=5,
       model=Category,
     )),

     # Tags
     url(r'tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
       paginate_by=5,
       model=Tag,
       )),
    
    # Media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}),

    url(r'^admin/', include(admin.site.urls)),
)
