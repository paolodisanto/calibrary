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
    magnitude = forms.ChoiceField(
        choices=[('', '---------')] + Tag.OPTIONS_MAGNITUDE,
        required=True,
        label='Magnitud'
    )
    technology = forms.ChoiceField(
        choices=[('', '---------')] + Tag.OPTIONS_TECHNOLOGY,
        required=True,
        label='Tecnología'
    )
    display = forms.ChoiceField(
        choices=[('', '---------')] + Tag.OPTIONS_DISPLAY,
        required=True,
        label='Display'
    )
    description = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = Instrument
        #fields = ['tag', 'location', 'location_comments', 'brand', 'model', 'range', 'unit', 'process_connection', 'serial_number', 'traceable', 'removal_date', 'removal_reason']
        fields = [
            'magnitude', 'technology', 'display', 'description', 'location',
            'location_comments', 'brand', 'model', 'range', 'unit', 'process_connection',
            'serial_number', 'traceable', 'removal_date', 'removal_reason'
            ]
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Editing an existing instance
            self.fields['magnitude'].initial = self.instance.tag.magnitude
            self.fields['technology'].initial = self.instance.tag.technology
            self.fields['display'].initial = self.instance.tag.display
            self.fields['description'].initial = self.instance.tag.description
        else:  # Creating a new instance
            self.fields['magnitude'].initial = ''
            self.fields['technology'].initial = ''
            self.fields['display'].initial = ''
            self.fields['description'].initial = ''

    def save(self, commit=True):
        instrument = super().save(commit=False)
        magnitude = self.cleaned_data['magnitude']
        technology = self.cleaned_data['technology']
        display = self.cleaned_data['display']
        description = self.cleaned_data['description']

        if not self.instance.pk:  # If creating a new instance
            tag = Tag.create_with_sequential_id(
                magnitude=magnitude,
                technology=technology,
                display=display,
                description=description
            )
            instrument.tag = tag
        else:
            tag = self.instance.tag
            tag.magnitude = magnitude
            tag.technology = technology
            tag.display = display
            tag.description = description
            tag.save()

        if commit:
            instrument.save()

        return instrument