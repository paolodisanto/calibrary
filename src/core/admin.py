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

class SetUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'date', 'gdc_type', 'gdc_number', 'author', 'alarm_set', 'trip_set', 'comments') #columnas que muestro    

class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'date', 'result', 'author', 'comments') #columnas que muestro    

class PatternInstrumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'calibration_date', 'calibration_lab', 'calibration_number', 'comments') #columnas que muestro 

class ContrastAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'date', 'result', 'author', 'expiration', 'p_instrument', 'comments') #columnas que muestro    

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'table_instance', 'media_path', 'name', 'uploaded_at', 'comments') #columnas que muestro 


admin.site.register(SequentialTag, SequentialTagAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Location)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(SetUp, SetUpAdmin)
admin.site.register(Check, CheckAdmin)
admin.site.register(PatternInstrument, PatternInstrumentAdmin)
admin.site.register(Contrast, ContrastAdmin)
admin.site.register(Attachment, AttachmentAdmin)