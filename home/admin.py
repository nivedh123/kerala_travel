from django.contrib import admin

from home.models import districts, remark, spot,reviewmodel

# Register your models here.
admin.site.register(spot)
admin.site.register(districts)
admin.site.register(remark)
admin.site.register(reviewmodel)