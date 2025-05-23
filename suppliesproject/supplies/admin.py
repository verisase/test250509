from django.contrib import admin

# Register your models here.
from .models import Supplies,Review

admin.site.register(Supplies)
admin.site.register(Review)