from django.contrib import admin
from .models import (
    Category, Brand, Product, HeroSection, 
    PromoSection, BlogPost, SiteSettings, ShowcaseModel
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'stock_status', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'brand', 'stock_status', 'is_featured', 'is_new', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = []
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('Kategori ve Marka', {
            'fields': ('category', 'brand')
        }),
        ('Fiyat ve Stok', {
            'fields': ('price', 'old_price', 'stock_status', 'stock_quantity')
        }),
        ('Görseller', {
            'fields': ('main_image', 'image_2', 'image_3')
        }),
        ('Özellikler', {
            'fields': ('weight', 'dimensions', 'material', 'color', 'size')
        }),
        ('Durumlar', {
            'fields': ('is_featured', 'is_new', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['sort_order']


@admin.register(PromoSection)
class PromoSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['sort_order']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']


@admin.register(ShowcaseModel)
class ShowcaseModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'topic', 'description']
    ordering = ['sort_order', 'created_at']
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'topic', 'description')
        }),
        ('3D Model', {
            'fields': ('sketchfab_model_id',),
            'description': 'Sketchfab Model ID kullanarak 3D model gösterimi. Model ID\'yi Sketchfab paylaşım linkinden alabilirsiniz.'
        }),
        ('Buton Ayarları', {
            'fields': ('button_text', 'button_url')
        }),
        ('Görünüm', {
            'fields': ('badge_text', 'is_active', 'sort_order')
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Genel Ayarlar', {
            'fields': ('site_name', 'site_description', 'logo', 'favicon')
        }),
        ('İletişim', {
            'fields': ('email', 'phone', 'whatsapp')
        }),
        ('Sosyal Medya', {
            'fields': ('instagram_url', 'youtube_url')
        }),
        ('Güven Mesajları', {
            'fields': ('trust_message_1', 'trust_message_2', 'trust_message_3')
        }),
    )

    def has_add_permission(self, request):
        # Sadece bir tane SiteSettings objesi olabilir
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # SiteSettings silinemez
        return False