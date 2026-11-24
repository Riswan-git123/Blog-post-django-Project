from django.contrib import admin
from .models import Post, category, AboutUs

class Postadmin(admin.ModelAdmin):
    list_display=('title', 'content')
    search_fields=('title', 'content')
    


admin.site.register(Post, Postadmin)
admin.site.register(category)
admin.site.register(AboutUs)
# Register your models here.
