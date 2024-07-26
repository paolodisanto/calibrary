# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from core.models import Instrument
from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, "core/index.html")

"""def detail(request, tag_id):
    return HttpResponse("You're looking at instrument %s." % tag_id)
"""

"""
    def detail(request, tag_id):
    latest_question_list = get_object_or_404(Instrument, tag__id=tag_id)
    context = {"instrument": latest_question_list}
    return render(request, "core/index.html", context)
"""

def detail(request):
    tag_id=request.POST.get("tag_id", "")
    latest_question_list = get_object_or_404(Instrument, tag__id=tag_id)
    context = {"instrument": latest_question_list}
    return render(request, "core/detail.html", context)
