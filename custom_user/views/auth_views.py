from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import CustomUser as User

def login_view(request):
    # Nếu người dùng đã đăng nhập, chuyển hướng đến platform_accounts
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Đăng nhập thành công
            login(request, user)
            # Chuyển hướng đến `next` hoặc trang mặc định
            return redirect(request.GET.get('next') or '/')
        else:
            # Thông báo lỗi nếu không thành công
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
    
    # Nếu là GET, hiển thị trang đăng nhập
    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công')
    return redirect('login')

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
                password=password,
            )
            # Log user in
            login(request, user)
            messages.success(request, 'Đăng ký thành công')
            return redirect('platform_accounts')
            
    return render(request, 'pages/signup.html')
