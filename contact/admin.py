from django.contrib import admin
from django.contrib import admin
from .models import ContactModel


class ContactFormAdmin(admin.ModelAdmin):
    class Meta:
        model = ContactModel


admin.site.register(ContactModel, ContactFormAdmin)
