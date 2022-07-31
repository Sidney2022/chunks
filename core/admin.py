from django.contrib import admin

from .models import CsvChunk

class CsvChunkAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_id', 'file', 'upload_time')

admin.site.register(CsvChunk, CsvChunkAdmin)