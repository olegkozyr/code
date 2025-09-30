from django.contrib import admin

# Register your models here.
from .models import Post, PostAdmin

admin.site.register(Post, PostAdmin)
