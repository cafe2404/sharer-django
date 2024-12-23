from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.templatetags.static import static
from platforms.models import AccountCookie
from django.shortcuts import get_object_or_404

def modifiy_content(content,request):
    soup = BeautifulSoup(content, 'html.parser')
    # Kiểm tra nếu thẻ <head> không có, tạo mới thẻ <head>
    if not soup.head:
        head_tag = soup.new_tag('head')
        soup.insert(0, head_tag)
    else:
        head_tag = soup.head
        

    for link in soup.find_all("link", {"rel": ["icon", "apple-touch-icon"]}):
        link.decompose()

    # Thêm favicon 32x32
    favicon_32 = soup.new_tag('link', rel='icon', sizes='32x32', href=request.build_absolute_uri(static('images/favicon-32x32.png')))
    head_tag.append(favicon_32)

    # Thêm favicon 192x192
    favicon_192 = soup.new_tag('link', rel='icon', sizes='192x192', href=request.build_absolute_uri(static('images/favicon-192x192.png')))
    head_tag.append(favicon_192)

    # Thêm favicon cho Apple devices
    apple_touch_icon = soup.new_tag('link', rel='apple-touch-icon', href=request.build_absolute_uri(static('images/apple-touch-icon.png')))
    head_tag.append(apple_touch_icon)

    # Thêm thẻ <style> nếu cần
    style_tag = soup.new_tag('style')
    style_tag.string = "[data-id='4b5f6632'], [data-id='a458ff5'], [data-id='2e5adb0'], header, footer, .intercom-lightweight-app, .header-cap {display: none !important;}"
    head_tag.append(style_tag)
    return str(soup)
# Create your views here.

@csrf_exempt
@login_required
def reverse_proxy(request,cookie_id):
    
    cookie =  get_object_or_404(AccountCookie, id=cookie_id)
    base_url = "https://rankerfox.com/my-account/"
    query_params = request.GET.urlencode()  # chuyển các tham số GET thành chuỗi query
    if query_params:
        target_url = f"{target_url}?{query_params}"
    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'cookie':cookie.cookie,
    }
    if 'Authorization' in request.headers:
        headers['Authorization'] = request.headers['Authorization']
    if request.method == 'GET':
        response = requests.get(base_url, headers=headers)
        if 'text/html' in response.headers.get('Content-Type', ''):
            modified_content = modifiy_content(response.content,request)
            return HttpResponse(modified_content, content_type='text/html')