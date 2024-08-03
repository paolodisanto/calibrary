from django import forms
from core.models import Tag, Instrument

"""
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['magnitude', 'technology', 'display', 'description']
"""     
        
class TagInlineForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['magnitude', 'technology', 'display', 'description']
                

class InstrumentForm(forms.ModelForm):
    magnitude = forms.ChoiceField(choices=Tag.OPTIONS_MAGNITUDE, required=True)
    technology = forms.ChoiceField(choices=Tag.OPTIONS_TECHNOLOGY, required=True)
    display = forms.ChoiceField(choices=Tag.OPTIONS_DISPLAY, required=True)
    description = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = Instrument
        #fields = ['tag', 'location', 'location_comments', 'brand', 'model', 'range', 'unit', 'process_connection', 'serial_number', 'traceable', 'removal_date', 'removal_reason']
        fields = ['magnitude', 'technology', 'display', 'description', 'location', 'location_comments', 'brand', 'model', 'range', 'unit', 'process_connection', 'serial_number', 'traceable', 'removal_date', 'removal_reason']
        
    def save(self, commit=True):
        instrument = super().save(commit=False)
        magnitude = self.cleaned_data['magnitude']
        technology = self.cleaned_data['technology']
        display = self.cleaned_data['display']
        description = self.cleaned_data['description']
        
        tag = Tag.create_with_sequential_id(
            magnitude=magnitude,
            technology=technology,
            display=display,
            description=description
        )
        instrument.tag = tag
        
        if commit:
            instrument.save()
        
        return instrument