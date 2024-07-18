from django.contrib import admin
from core.models import (
    SequentialTag, Tag, Location, Instrument, SetUp,
    Check, PatternInstrument, Contrast, Attachment
)

class InstrumentAdmin(admin.ModelAdmin): #genero un modelo de admin para gestionar el modelo de la manera en que yo decida
    list_display = ('id', 'tag', 'brand', 'location') #aca pongo los campos a listar
    list_filter = ('location', 'brand') #filtro

admin.site.register(SequentialTag)
admin.site.register(Tag)
admin.site.register(Location)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(SetUp)
admin.site.register(Check)
admin.site.register(PatternInstrument)
admin.site.register(Contrast)
admin.site.register(Attachment)