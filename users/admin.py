from django.contrib import admin
from users.models import Customer, Counter
from rest_framework.authtoken.admin import TokenAdmin


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'phone', 'saldo',)
    search_fields = ['user']


class CounterAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'phone',)
    search_fields = ['user']

TokenAdmin.raw_id_fields = ('user',)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Counter, CounterAdmin)