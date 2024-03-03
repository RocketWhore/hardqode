from django.contrib import admin

from product.models import Product, Lesson, Group, Accessible

# Register your models here.
admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)
admin.site.register(Accessible)