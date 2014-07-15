from django.db import models

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()

  def __unicode__(self):
    return self.name
          
  class Meta:
    verbose_name_plural = 'categories'


class Post(models.Model):
  title = models.CharField(max_length=200)
  pub_date = models.DateTimeField()
  text = models.TextField()
  category = models.ForeignKey(Category, blank=True, null=True)


  def __unicode__(self):
    return self.title

  class Meta:
    ordering = ["-pub_date"]
