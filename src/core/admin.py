from django.contrib import admin
from django.contrib.admin import SimpleListFilter #Se agrega para poder realizar filtros personalizados en el admin de django
from django.utils.html import format_html
from .form import InstrumentForm #, TagForm
from core.models import (
    SequentialTag, Tag, Location, Instrument, SetUp,
    Check, PatternInstrument, Contrast, Attachment
)


class RemovalDateFilter(SimpleListFilter):
    """ 
    El instrumento se da de baja al poner fecha en el campo 'removal_date', 
    por este motivo se define un filtro personalizado para el campo 'removal_date', 
    listando solos los instrumentos "activos".
    """
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
    

class InstrumentAdmin(admin.ModelAdmin):
    form = InstrumentForm
    
    default_list_display = (
        'id', 'tag', 'get_tag_description', 'get_tag_magnitude_display', 'get_tag_technology_display',
        'get_tag_display_display', 'location', 'location_comments' , 'traceable'
    )
    
    additional_fields = ('removal_date', 'removal_reason')
    
    def get_list_display(self, request):
        
        if request.GET.get('removal_date') == 'Not None':
            return self.default_list_display + self.additional_fields
        
        return self.default_list_display
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # If editing an existing instance
            form.base_fields['magnitude'].initial = obj.tag.magnitude
            form.base_fields['technology'].initial = obj.tag.technology
            form.base_fields['display'].initial = obj.tag.display
            form.base_fields['description'].initial = obj.tag.description
        else:  # If creating a new instance
            form.base_fields['magnitude'].initial = ''
            form.base_fields['technology'].initial = ''
            form.base_fields['display'].initial = ''
            form.base_fields['description'].initial = ''
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
    
        if 'removal_date' not in request.GET and not request.resolver_match.kwargs:
            return qs.filter(removal_date__isnull=True)
        
        return qs.select_related('tag')
        
    list_select_related = ('tag',)  # Optimiza la consulta para incluir datos relacionados
    
    @admin.display(description='Description')
    def get_tag_description(self, obj):
        
        return obj.tag.description
    
    @admin.display(description='Magnitude')
    def get_tag_magnitude_display(self, obj):
        
        return obj.tag.get_magnitude_display()
    
    @admin.display(description='Technology')
    def get_tag_technology_display(self, obj):
        
        return obj.tag.get_technology_display()

    @admin.display(description='Display')
    def get_tag_display_display(self, obj):
        
        return obj.tag.get_display_display()   
    
    list_filter = (RemovalDateFilter, 'traceable', 'location')


class SequentialTagAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'latest')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'magnitude', 'technology', 'display', 'description', 'qr_code_image')
    list_filter = ('id', 'magnitude', 'technology', 'display', 'description')
    actions = ['generate_qr_codes']
    readonly_fields = ('qr_code',)
    #form = TagForm
    #readonly_fields = ['id']

    def generate_qr_codes(self, request, queryset):
        for tag in queryset:
            if not tag.qr_code:
                tag.save()
        self.message_user(request, "Códigos QR generados/actualizados correctamente.")
    generate_qr_codes.short_description = "Generar QR codes para tags seleccionados"

    def qr_code_image(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.qr_code.url))
        return "No QR code"
    qr_code_image.short_description = "QR Code"

    """
    def save_model(self, request, obj, form, change):
        if not change:
            # Solo generar el ID si es un nuevo objeto
            obj.id = Tag.create_with_sequential_id(
                magnitude=form.cleaned_data['magnitude'],
                technology=form.cleaned_data['technology'],
                display=form.cleaned_data['display'],
                description=form.cleaned_data['description']
            ).id
        super().save_model(request, obj, form, change)
"""

class SetUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'date', 'gdc_type', 'gdc_number', 'author', 'alarm_set', 'trip_set', 'comments')
   

class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'date', 'result', 'author', 'comments')


class PatternInstrumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'calibration_date', 'calibration_lab', 'calibration_number', 'comments')


class ContrastAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'date', 'result', 'author', 'expiration', 'p_instrument', 'comments')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'table_instance', 'media_path', 'name', 'uploaded_at', 'comments')


admin.site.register(SequentialTag, SequentialTagAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Location)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(SetUp, SetUpAdmin)
admin.site.register(Check, CheckAdmin)
admin.site.register(PatternInstrument, PatternInstrumentAdmin)
admin.site.register(Contrast, ContrastAdmin)
admin.site.register(Attachment, AttachmentAdmin)