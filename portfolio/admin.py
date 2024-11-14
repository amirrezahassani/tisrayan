from django.contrib import admin
from .models import PF, Category, Tag


class PFAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_name', 'category', 'technology_used', 'slug')


admin.site.register(PF, PFAdmin)
admin.site.register(Category)
admin.site.register(Tag)
