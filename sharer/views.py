from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def default_view(request):
    if request.user.is_authenticated:
        return redirect('platform_accounts')  # Tên của view hoặc tên URL pattern bạn muốn chuyển hướng
    else:
        return redirect('login')  # Tên URL pattern của trang đăng nhập
