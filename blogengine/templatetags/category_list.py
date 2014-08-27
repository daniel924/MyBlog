from django import template
from blogengine.models import Category, Post, Tag

register = template.Library()

@register.inclusion_tag('category_nav_list.html')
def get_categories():
  categories = Category.objects.all()
  return {'categories': categories}

