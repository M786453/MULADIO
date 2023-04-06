from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def muladio(request):

    tempate = loader.get_template('muladio.html')

    return HttpResponse(tempate.render())
