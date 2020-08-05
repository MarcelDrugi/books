from django.shortcuts import render
from django.views.generic import TemplateView


class InfoView(TemplateView):
    template_name = 'books/info.html'
