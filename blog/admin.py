from django.contrib import admin
from .models import blogmodel,reviewmodel_blog
# Register your models here.
admin.site.register(blogmodel)
admin.site.register(reviewmodel_blog)