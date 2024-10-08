from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound
from core.models import Instrument, Tag , Attachment
from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    return render(request, "core/index.html")

def get_instrument_context(tag_id):
    """
    Función auxiliar para manejar la recuperación de datos.
    Me permite llamarla después desde dos vistas (detail e instrument_detail).
    """
    try:
        instrument = Instrument.objects.get(tag__id=tag_id)
    except Instrument.DoesNotExist:
        return None  # Indicar que no se encontró el instrumento
    
    checks = instrument.checks.all()
    contrasts = instrument.contrasts.all()
    setups = instrument.setups.all()

    latest_check = checks.order_by('-date').first()
    latest_contrast = contrasts.order_by('-date').first()
    latest_alarm_setup = setups.filter(alarm_set__isnull=False).order_by('-date').first()
    latest_trip_setup = setups.filter(trip_set__isnull=False).order_by('-date').first()
    
    instrument_content_type = ContentType.objects.get_for_model(Instrument)
    attachments = Attachment.objects.filter(
        table=instrument_content_type,
        table_instance=instrument.id
    )


    return {
        'instrument': instrument,
        'checks': checks,
        'contrasts': contrasts,
        'setups': setups,
        'latest_check': latest_check,
        'latest_contrast': latest_contrast,
        'latest_alarm': latest_alarm_setup,
        'latest_trip': latest_trip_setup,
        'attachments': attachments,
    }

def search_item(request, qr_value=None):
    if not qr_value:
        qr_value = request.POST.get('qr_value')
    
    context = get_instrument_context(qr_value)
    if context is None:
        return render(request, 'core/search_item.html', {'error_message': 'QR inválido. Por favor, intente nuevamente.'})
    
    return render(request, 'core/instrument.html', context)

def instrument_detail(request, tag_id):
    context = get_instrument_context(tag_id)
    if context is None:
        return render(request, 'core/instrument_detail.html', {'error_message': 'Instrumento no encontrado. Por favor, intente nuevamente.'})
    
    return render(request, 'core/instrument_detail.html', context)

def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    if request.method == 'POST':
        attachment.delete()
        return redirect('instrument_detail', tag_id=attachment.content_object.tag.id)
    return redirect('instrument_detail', tag_id=attachment.content_object.tag.id)