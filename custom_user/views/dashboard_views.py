from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from subscriptions.models import PackageToken
from ..serializers import  AccountSerializer , UserSubscriptionSerializer
from platforms.models import Account
from subscriptions.serializers import PackageSerializer
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def settings_view(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            # Handle email update
            new_email = request.POST.get('email')
            if new_email:
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Email đã được cập nhật')
                return redirect('settings')
                
        elif 'current_password' in request.POST:
            # Handle password change (existing code)
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            user = authenticate(username=request.user.username, password=current_password)
            if user is None:
                messages.error(request, 'Mật khẩu hiện tại không đúng')
            elif new_password != confirm_password:
                messages.error(request, 'Mật khẩu mới không khớp')
            elif len(new_password) < 8:
                messages.error(request, 'Mật khẩu mới phải có ít nhất 8 ký tự')
            else:
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request, 'Đổi mật khẩu thành công')
                return redirect('settings')
                
        elif 'delete_account' in request.POST:
            # Handle account deletion
            user = request.user
            user.delete()
            messages.success(request, 'Tài khoản đã được xóa')
    return render(request, 'pages/dashboard/settings.html')
def dashboard_view(request):
    user = request.user

    # Kiểm tra người dùng có gói đăng ký hay không
    package_token = PackageToken.objects.filter(user=user, is_active=True).first()

    # Lấy gói đăng ký của người dùng
    package = package_token.package

    # Lấy tài khoản của người dùng (cả tài khoản thuộc gói và không thuộc gói)
    accounts = Account.objects.filter(rented_by=user)

    # Serialize thông tin người dùng, gói đăng ký và tài khoản của họ
    user_subscription_serializer = UserSubscriptionSerializer(user)
    package_serializer = PackageSerializer(package)
    account_serializer = AccountSerializer(accounts, many=True)
    return render(
        request, 'pages/dashboard/dashboard.html',
        {
            'user_subscription': user_subscription_serializer.data,
            'package': package_serializer.data,
            'accounts': account_serializer.data,
        }
    )

def subscription_view(request):
    return render(request, 'pages/dashboard/subscriptions.html')


@login_required
def transaction_history_view(request):
    # Lấy danh sách giao dịch của người dùng hiện tại
    user = request.user
    transactions = Order.objects.filter(user=user).order_by('-created_at')  # Sắp xếp theo thời gian giảm dần

    # Sử dụng Paginator
    paginator = Paginator(transactions, 10)  # Hiển thị tối đa 10 dòng trên mỗi trang
    page_number = request.GET.get('page', 1)  # Lấy số trang từ query string
    page_obj = paginator.get_page(page_number)  # Lấy danh sách giao dịch cho trang hiện tại
    is_paginated = paginator.num_pages > 1
    context = {
        'page_obj': page_obj,  
        'is_paginated': is_paginated,
    }
    return render(request, 'pages/dashboard/transaction_history.html', context)

