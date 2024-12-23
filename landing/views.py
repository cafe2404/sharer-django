from django.shortcuts import render
from django.views import View
from .models import LandingPageContent, FooterColumn
class LandingPageView(View):
    def get(self, request):
        landing = LandingPageContent.objects.filter(is_active=True).first()
        footers = FooterColumn.objects.all()
        return render(request, 
            'pages/landing_page.html',{
            "landing":landing,
            "footers": footers
        })