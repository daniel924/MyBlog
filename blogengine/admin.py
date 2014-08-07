import models
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("title",)}

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)
