from django.contrib import admin

from crud_google_sheet.models import Orders


# Register your models here.
@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = [f'{f.name}' for f in Orders._meta.get_fields()]