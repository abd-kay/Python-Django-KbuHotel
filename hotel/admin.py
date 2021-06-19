from django.contrib import admin

# Register your models here.
from hotel.models import Category, Hotel, Images


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status', 'update_at']
    list_filter = ['status']

class HotelImageInline(admin.TabularInline):
    model = Images
    extra = 3

class HotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'update_at']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [HotelImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(Images,ImagesAdmin)
