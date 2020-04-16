from django.contrib import admin

# Register your models here.
from document.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_time', 'input_meta_data')
    ordering = ('owner',)
    search_fields = ('owner', 'type')
