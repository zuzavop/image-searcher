from django.shortcuts import render, HttpResponse
from var import clip_data


def index(request):
    return render(request, 'index.html')
