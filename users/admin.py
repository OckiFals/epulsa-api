from django.contrib import admin
from users.models import Customer
from rest_framework.authtoken.admin import TokenAdmin


class CustomerAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'': ('name',)}
    # list_display = ('', 'brewery', 'locality',)
    search_fields = ['phone']

TokenAdmin.raw_id_fields = ('user',)
admin.site.register(Customer, CustomerAdmin)