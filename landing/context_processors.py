from .models import SocialLink,LandingPageContent
def landing_context(request):
    facebook = SocialLink.objects.filter(is_active=True, platform='Facebook').first()
    telegram = SocialLink.objects.filter(is_active=True, platform='Telegram').first()
    zalo = SocialLink.objects.filter(is_active=True, platform='Zalo').first()
    landing = LandingPageContent.objects.filter(is_active=True).order_by('-id').first()
    return {
        'facebook': facebook,
        'telegram': telegram,
        'zalo': zalo,
        'landing':landing
    }