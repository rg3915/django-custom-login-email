from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


# @login_required
def index(request):
    return HttpResponse('<h1>Django</h1><p>Página simples.</p>')
