from django.contrib import admin

from home.models import districts, remark, spot,reviewmodel,profilemodel,cluster

class spotAdmin(admin.ModelAdmin):
    list_display=('name','verify','district','date')
class reviewAdmin(admin.ModelAdmin):
    list_display=('spot','user','rating','date')
class profileAdmin(admin.ModelAdmin):
    list_display=('Name','user','verify')
class clusterAdmin(admin.ModelAdmin):
    list_display=('name','publish')
# Register your models here.
admin.site.register(spot,spotAdmin)
admin.site.register(districts)
admin.site.register(remark)
admin.site.register(reviewmodel)
admin.site.register(profilemodel,profileAdmin)
admin.site.register(cluster,clusterAdmin)
