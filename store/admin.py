from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Banner


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'slug', 'is_active', 'product_count', 'created_at')
    list_display_links = ('image_preview', 'name')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview_large', 'created_at')
    fields = ('name', 'slug', 'image', 'image_preview_large', 'is_active', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 8px; border: 1px solid #e5e7eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af; font-size: 11px;">No Image</span>')
    image_preview.short_description = 'Thumbnail'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 180px; max-width: 260px; object-fit: contain; border-radius: 8px; border: 1px solid #e5e7eb;" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No Image Uploaded</span>')
    image_preview_large.short_description = 'Current Image Preview'

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Total Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'in_stock', 'is_featured', 'is_active', 'created_at')
    list_display_links = ('image_preview', 'name')
    list_editable = ('is_active', 'is_featured', 'in_stock')
    list_filter = ('is_active', 'is_featured', 'in_stock', 'category', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview_large', 'created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'price', 'description')
        }),
        ('Media', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Visibility & Promotion', {
            'fields': ('is_active', 'is_featured', 'in_stock')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 8px; border: 1px solid #e5e7eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af; font-size: 11px;">No Image</span>')
    image_preview.short_description = 'Thumbnail'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 240px; max-width: 360px; object-fit: contain; border-radius: 8px; border: 1px solid #e5e7eb;" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No Image Uploaded</span>')
    image_preview_large.short_description = 'Current Image Preview'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'subtitle', 'button_text', 'order', 'is_active')
    list_display_links = ('image_preview', 'title')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'button_text')
    readonly_fields = ('image_preview_large',)
    fields = ('title', 'subtitle', 'image', 'image_preview_large', 'button_text', 'button_link', 'order', 'is_active')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 90px; height: 45px; object-fit: cover; border-radius: 6px; border: 1px solid #e5e7eb;" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af; font-size: 11px;">No Image</span>')
    image_preview.short_description = 'Thumbnail'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 480px; object-fit: cover; border-radius: 8px; border: 1px solid #e5e7eb;" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No Image Uploaded</span>')
    image_preview_large.short_description = 'Current Image Preview'
