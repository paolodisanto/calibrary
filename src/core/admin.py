from django.contrib import admin
from django.contrib.admin import SimpleListFilter #se agrega para poder realizar filtros personalizados en el admin de django
from core.models import (
    SequentialTag, Tag, Location, Instrument, SetUp,
    Check, PatternInstrument, Contrast, Attachment
)

""" 
El instrumento se da de baja al poner fecha en el campo 'removal_date', 
por este motivo se define un filtro personalizado para el campo 'removal_date', 
listando solos los instrumentos "activos".
"""
class RemovalDateFilter(SimpleListFilter):
    title = 'removal date'
    parameter_name = 'removal_date'

    def lookups(self, request, model_admin):
        return (
            ('None', 'No removal date'),
            ('Not None', 'With removal date'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'None':
            return queryset.filter(removal_date__isnull=True)
        if self.value() == 'Not None':
            return queryset.filter(removal_date__isnull=False)
        return queryset


class InstrumentAdmin(admin.ModelAdmin): #genero un modelo de admin para gestionar el modelo de la manera en que yo decida
    #defino los campos a mostrar por defecto
    default_list_display = (
        'id', 'tag', 'get_tag_magnitude_display', 'location', 'location_comments', 'brand', 'model',
        'range', 'unit', 'process_connection', 'serial_number', 'traceable'
    )
    additional_fields = ('removal_date', 'removal_reason') #agrego los campos extras que voy a mostrar solo para instrumentos dados de baja
    
    def get_list_display(self, request):
        # Verifica si el filtro 'removal_date' está activo y su valor
        if request.GET.get('removal_date') == 'Not None':
            return self.default_list_display + self.additional_fields #en caso de que removal_date tenga un valor, se listan con mas campos
        return self.default_list_display
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Aplica el filtro por defecto solo si no se ha seleccionado ningún filtro
        if not request.GET.get('removal_date'):
            return qs.filter(removal_date__isnull=True)
        return qs.select_related('tag') # Usa select_related para optimizar la consulta
    
    list_select_related = ('tag',)  # Optimiza la consulta para incluir datos relacionados
    
    @admin.display(description='TAG Magnitude')
    def get_tag_magnitude_display(self, obj):
        return obj.tag.get_magnitude_display()    
    
    list_filter = (RemovalDateFilter, 'traceable', 'location')

    #ver en chat como listar campos pero que sean vinculos
    #list_filter = ('location', 'brand') #filtro
    
    #ver en chat como editar el admin de django para poner logos

class SequentialTagAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'latest') #columnas que muestro

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'magnitude', 'technology', 'display', 'description') #columnas que muestro
    list_filter = ('id', 'magnitude', 'technology', 'display', 'description') #filtro

class SetUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'brand', 'date', 'gdc_type', 'gdc_number', 'author', 'alarm_set', 'trip_set', 'comments') #columnas que muestro    
   #como ejemplo agrege brand en el modelo de SetUp para poder mostrarlo.

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