from django.contrib import admin
from .models import User, categories, Products, Cart, ProductReview, Payment,Order

admin.site.register(User)
admin.site.register(categories)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(ProductReview)
admin.site.register(Payment)
admin.site.register(Order)
