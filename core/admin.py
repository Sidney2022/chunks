from django.contrib import admin

from .models import CsvChunk

class CsvChunkAdmin(admin.ModelAdmin):
    list_display = ('user', 'chunk_id', 'file')

admin.site.register(CsvChunk, CsvChunkAdmin)