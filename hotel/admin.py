from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
# Register your models here.
from hotel.models import Category, Hotel, Images


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status', 'update_at', 'image_tag']
    list_filter = ['status']



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_hotels_count', 'related_hotels_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative hotel count
        qs = Category.objects.add_related_count(
                qs,
                Hotel,
                'category',
                'hotels_cumulative_count',
                cumulative=True)

        # Add non cumulative hotel count
        qs = Category.objects.add_related_count(qs,
                 Hotel,
                 'category',
                 'hotels_count',
                 cumulative=False)
        return qs

    def related_hotels_count(self, instance):
        return instance.hotels_count
    related_hotels_count.short_description = 'Related hotels (for this specific category)'

    def related_hotels_cumulative_count(self, instance):
        return instance.hotels_cumulative_count
    related_hotels_cumulative_count.short_description = 'Related hotels (in tree)'

class HotelImageInline(admin.TabularInline):
    model = Images
    extra = 3

class HotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'update_at', 'image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [HotelImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title']


admin.site.register(Category,CategoryAdmin2)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(Images,ImagesAdmin)
