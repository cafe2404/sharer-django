from django.shortcuts import render

def handler404(request, exception):
    """
    Custom 404 error handler that renders the 404.html template
    """
    return render(request, '404.html', status=404)
