from django.shortcuts import render
from django.views import View
from subscriptions.models import SubscriptionPlan, Package
from .models import LandingPageContent
class LandingPageView(View):
    def get(self, request):
        landing = LandingPageContent.objects.filter(is_active=True).first()
        return render(request, 
            'pages/landing_page.html',{
            "landing":landing
        })