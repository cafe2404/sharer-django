from django.urls import reverse
from django.shortcuts import redirect

def verification_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.verificationcode_set.filter(is_verified=True).exists():
                next_url = request.path
                if request.path != reverse('verification_email'):
                    return redirect(f"{reverse('verification_email')}?next={next_url}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
