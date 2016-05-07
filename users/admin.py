from django.contrib import admin
from users.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'': ('name',)}
    # list_display = ('', 'brewery', 'locality',)
    search_fields = ['phone']


admin.site.register(Customer, CustomerAdmin)