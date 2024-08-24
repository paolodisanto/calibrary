#import qrcode
#from io import BytesIO
from django.http import HttpResponse
from core.models import Instrument
from django.shortcuts import render, get_object_or_404
#from django.urls import reverse

def index(request):
    return render(request, "core/index.html")

#def scan_qr(request):
#    return render(request, 'core/scan_qr.html')
def search_item(request, qr_value=None):
    if not qr_value:
        qr_value = request.POST.get('qr_value')
    instrument = get_object_or_404(Instrument, tag__id=qr_value)
    return render(request, 'core/detail.html', {'instrument': instrument})
    
"""def detail(request):
    tag_id=request.POST.get("tag_id", "")
    latest_question_list = get_object_or_404(Instrument, tag__id=tag_id)
    context = {"instrument": latest_question_list}
    return render(request, "core/detail.html", context)
"""

"""def detail(request, tag_id):
    return HttpResponse("You're looking at instrument %s." % tag_id)
"""

"""
    def detail(request, tag_id):
    latest_question_list = get_object_or_404(Instrument, tag__id=tag_id)
    context = {"instrument": latest_question_list}
    return render(request, "core/index.html", context)
"""

"""
def generate_qr(request, tag):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(tag)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')

    # Save the image in a BytesIO buffer
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the image as a response
    return HttpResponse(buffer, content_type='image/png')

def qr_code_view(request):
    tag = "TSI-001"
    qr_url = reverse('generate_qr', kwargs={'tag': tag})
    return render(request, 'myapp/qr_code.html', {'qr_url': qr_url})
"""

def instrument_detail(request, tag_id):
    instrument = get_object_or_404(Instrument, tag__id=tag_id)
    
    checks = instrument.checks.all()
    contrasts = instrument.contrasts.all()
    setups = instrument.setups.all()

    # Obtener la última instancia de SetUp
    latest_setup = setups.order_by('-date').first()

    context = {
        'instrument': instrument,
        'checks': checks,
        'contrasts': contrasts,
        'setups': setups,
        'latest_setup': latest_setup,
    }
    
    return render(request, 'core/instrument_detail.html', context)