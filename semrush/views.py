from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import PlatformAccount
import requests
from django.http import HttpResponse,JsonResponse
from .custom_platform import CustomPlatform
from django.db import models


# Create your views here.
@login_required
def platform_accounts(request):
    platform_accounts = PlatformAccount.objects.filter(
                            models.Q(users=request.user) | 
                            models.Q(groups__users=request.user)
                        ).distinct()
    return render(request, 'pages/platform_accounts.html', {'platform_accounts': list(platform_accounts)})

@login_required
def platform_account_detail(request,account_id):
    if request.method == 'GET':
        platform_account = PlatformAccount.objects.filter(id=account_id).first()
        return JsonResponse(platform_account.to_dict())
    else:
        return JsonResponse({'error': 'Invalid request method'})
def prepare_headers(self, request):
    """Prepares headers to forward to the target server."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': request.headers.get('Content-Type'),
    }
    if 'Authorization' in request.headers:
        headers['Authorization'] = request.headers['Authorization']
    return headers

@csrf_exempt
def reverse_proxy_semrush(request, path=''):
    platform_account = PlatformAccount.objects.filter(id=1).first()
    if not platform_account:
        return redirect('platform_accounts')

    base_url = platform_account.platform.url
    target_url = f"{base_url}/{path}"
        # Lấy các query parameters từ request
    query_params = request.GET.urlencode()  # chuyển các tham số GET thành chuỗi query
    if query_params:
        target_url = f"{target_url}?{query_params}"
    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'cookie': platform_account.cookie,
    }
    if 'Authorization' in request.headers:
        headers['Authorization'] = request.headers['Authorization']
    if request.method == 'GET':
        response = requests.get(target_url, headers=headers)
        if response.status_code in [301, 302]:
            target_url = response.headers['Location']
            response = requests.get(target_url, headers=headers)
        # Chuyển đổi URL tài nguyên
        if 'text/html' in response.headers.get('Content-Type', ''):
            modified_content = CustomPlatform.parser_html(platform_account.platform,response.text)
            return HttpResponse(modified_content, content_type='text/html')
        
        else:
            return HttpResponse(response.content, content_type=response.headers['Content-Type'])
        
    elif request.method == 'POST':
        headers['Content-Type'] = request.headers.get('Content-Type')
        if 'application/json' in headers['Content-Type']:
            data = json.loads(request.body)
            response = requests.post(target_url, headers=headers, json=data)
            return JsonResponse(response.json(), safe=False)
        else:
            response = requests.post(target_url, headers=headers, data=request.body)
            return HttpResponse(response.content, content_type=response.headers['Content-Type'])
