from django.http import HttpResponse
from core.models import Instrument, SetUp
from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, "core/index.html")

def get_instrument_context(tag_id):
    """
    Funcion auxiliar para manejar la recuperacion de datos.
    Me permite llamarla depues desde dos vistas (detail y intrumenet_detail)
    """
    instrument = get_object_or_404(Instrument, tag__id=tag_id)
    
    checks = instrument.checks.all()
    contrasts = instrument.contrasts.all()
    setups = instrument.setups.all()
    
    
    latest_check = checks.order_by('-date').first()
    latest_contrast = contrasts.order_by('-date').first()
    #latest_setup = setups.order_by('-date').first()
    latest_alarm_setup = setups.filter(alarm_set__isnull=False).order_by('-date').first()
    latest_trip_setup = setups.filter(trip_set__isnull=False).order_by('-date').first()
    


    return {
        'instrument': instrument,
        'checks': checks,
        'contrasts': contrasts,
        'setups': setups,
        'latest_check': latest_check,
        'latest_contrast': latest_contrast,
        #'latest_setup': latest_setup,
        'latest_alarm': latest_alarm_setup,
        'latest_trip': latest_trip_setup,
    }

def search_item(request, qr_value=None):
    if not qr_value:
        qr_value = request.POST.get('qr_value')
    context = get_instrument_context(qr_value)
    return render(request, 'core/detail.html', context)

def instrument_detail(request, tag_id):
    context = get_instrument_context(tag_id)
    return render(request, 'core/instrument_detail.html', context)