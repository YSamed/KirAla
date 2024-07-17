from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, ProductFeature, ProductFeatureValue, Marketing

class ProductFeatureValueInline(admin.TabularInline):
    model = ProductFeatureValue
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active', 'category_hierarchy')
    list_filter = ('is_active',)
    inlines = [ProductFeatureValueInline]

    def category_hierarchy(self, obj):
        return ' -> '.join([cat.name for cat in obj.category.get_ancestors(include_self=True)])

class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name',)
    list_display_links = ('indented_title',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductFeature)
admin.site.register(Marketing)
