from django.contrib import admin
from .models import Product,Brand,Category,Comment
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'product', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)