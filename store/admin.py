from django.contrib import admin
from .models import Phone, Customer



class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock', 'release_date')  # Added release_date
    search_fields = ('name', 'brand')

# Register your models here.
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Customer)