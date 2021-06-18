from django.contrib import admin

# Register your models here.
from hotel.models import Category, Hotel

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status', 'update_at']
    list_filter = ['status']

class HotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'update_at']
    list_filter = ['category']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Hotel,HotelAdmin)