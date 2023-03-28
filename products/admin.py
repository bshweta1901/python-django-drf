from django.contrib import admin
from .models import Brands,Products,Imaget,Color,Size,Variants

# Register your models here.

admin.site.register(Brands)
admin.site.register(Imaget)
admin.site.register(Products)

admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variants)