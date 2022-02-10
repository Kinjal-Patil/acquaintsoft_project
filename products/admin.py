from django.contrib import admin

# Register your models here.
from products.models import *

admin.site.register(Products)
admin.site.register(Category)
