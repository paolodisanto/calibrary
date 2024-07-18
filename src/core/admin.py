from django.contrib import admin
from core.models import (
    SequentialTag, Tag, Location, Instrument, SetUp,
    Check, PatternInstrument, Contrast, Attachment
)

class InstrumentAdmin(admin.ModelAdmin): #genero un modelo de admin para gestionar el modelo de la manera en que yo decida
    list_display = ('id', 'tag', 'location', 'location_comments', 'brand', 'model', 'range', 'unit', 'process_connection', 'serial_number', 'traceable', 'removal_date', 'removal_reason') #aca pongo los campos a listar
    #ver en chat como listar campos pero que sean vinculos
    #list_filter = ('location', 'brand') #filtro
    
    #ver en chat como editar el admin de django para poner logos

class SequentialTagAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'latest') #columnas que muestro

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'magnitude', 'technology', 'display', 'description') #columnas que muestro
    list_filter = ('id', 'magnitude', 'technology', 'display', 'description') #filtro
    

admin.site.register(SequentialTag, SequentialTagAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Location)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(SetUp)
admin.site.register(Check)
admin.site.register(PatternInstrument)
admin.site.register(Contrast)
admin.site.register(Attachment)