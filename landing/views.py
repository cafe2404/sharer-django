from django.shortcuts import render
from django.views import View
from .models import LandingPageContent, FooterColumn

class LandingPageView(View):
    def get(self, request):
        footers = FooterColumn.objects.all()
        return render(request, 
            'pages/landing_page.html',{
            "footers": footers
        })