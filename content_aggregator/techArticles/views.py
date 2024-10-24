from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from .models import Article

# Create your views here.

class HomePageView(ListView):
    template_name = "homepage.html"
    model = Article
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter().order_by("-pubDate") [:10]
        return context
        