from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser as User
def login_view(request):
    # Nếu người dùng đã đăng nhập, chuyển hướng đến platform_accounts
    if request.user.is_authenticated:
        return redirect('platform_accounts')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Đăng nhập thành công
            login(request, user)
            # Chuyển hướng đến `next` hoặc trang mặc định
            return redirect(request.GET.get('next') or 'platform_accounts')
        else:
            # Thông báo lỗi nếu không thành công
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
    
    # Nếu là GET, hiển thị trang đăng nhập
    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công')
    return redirect('login')

def settings_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Kiểm tra mật khẩu hiện tại
        user = authenticate(username=request.user.username, password=current_password)
        
        if user is None:
            messages.error(request, 'Mật khẩu hiện tại không đúng')
        elif new_password != confirm_password:
            messages.error(request, 'Mật khẩu mới không khớp')
        elif len(new_password) < 8:
            messages.error(request, 'Mật khẩu mới phải có ít nhất 8 ký tự')
        else:
            # Đổi mật khẩu
            user.set_password(new_password)
            user.save()
            # Đăng nhập lại với mật khẩu mới
            login(request, user)
            messages.success(request, 'Đổi mật khẩu thành công')
            return redirect('settings')
    return render(request, 'pages/settings.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('platform_accounts')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate input
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên người dùng đã tồn tại')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng')
        elif password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp')
        elif len(password) < 8:
            messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự')
        else:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Log user in
            login(request, user)
            messages.success(request, 'Đăng ký thành công')
            return redirect('platform_accounts')
            
    return render(request, 'pages/signup.html')
