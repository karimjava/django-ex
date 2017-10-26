# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader


def test(request):
    return HttpResponse('hi')


def index(request):
    # template = loader.get_template("templates/index.html")
    try:
        return render(request, 'index.html')
    except Exception as e:
        print e
        return HttpResponse('hi')
