from django.contrib import admin
from .models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ['user','vendor_name','vendor_license','is_approved','created_at','modified_at']
    list_editable = ['is_approved']
    list_display_links = ['user','vendor_name']
    

admin.site.register(Vendor, VendorAdmin)