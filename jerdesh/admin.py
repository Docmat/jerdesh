from django.contrib import admin
from django.utils import timezone
from .models import Category, City, Ad


admin.site.register(Category)
admin.site.register(City)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
	now = timezone.now()
	list_display = ['ad_title', 'ad_text', 'author', 'category', 'city', 'img', 'pub_date']
	prepopulated_fields = {'slug': ('ad_title', 'author')}

