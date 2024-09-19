from django.contrib import admin
from product.models import Product, Size, Color, Category, Information, ContactUs, Comment, Rating, SaveProduct


class InformationAdmin(admin.StackedInline):
    model = Information


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price")
    inlines = (InformationAdmin,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("user", "email")


@admin.register(Rating)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")


@admin.register(SaveProduct)
class SaveProductAdmin(admin.ModelAdmin):
    list_display = ("user", "product")


admin.site.register(Size)
admin.site.register(Comment)
admin.site.register(Color)
