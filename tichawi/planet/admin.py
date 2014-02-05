from django.contrib import admin

# Register your models here.
from planet.models import Category, Feed

admin.site.register(Category)
admin.site.register(Feed)
