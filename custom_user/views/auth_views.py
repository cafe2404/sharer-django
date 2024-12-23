from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import CustomUser as User, VerificationCode
from django.http import JsonResponse
from ..forms  import SignupForm




def login_view(request):
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
        return redirect(request.GET.get('next') or '/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone_number
            )
            login(request, user)
            # messages.success(request, 'Kiểm tra email của bạn để xác thực')
            return redirect('verification_email')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'pages/signup.html', {'form': form})

@login_required
def verification_email_view(request):
    user: User = request.user
    if VerificationCode.objects.filter(user=user, is_verified=True).first():
        return redirect(request.GET.get('next') or '/')
    verification_code = VerificationCode.objects.filter(user=user, is_verified=False).first()
    
    if not verification_code:
        verification_code = VerificationCode.objects.create(user=user)
    else:
        if verification_code.is_code_expired():
            verification_code.code = verification_code.create_verification_code()
    if request.method == 'POST':
        code = request.POST.get('code')
        if not code:
            messages.error(request, 'Vui lòng nhập mã xác thực.')
        else:
            if verification_code.code == code :
                if verification_code.is_code_expired():
                    messages.error(request, 'Mã xác thực đã hết hạn, vui lòng tạo lại mã mới.')
                else:
                    verification_code.is_verified = True
                    verification_code.save()
                    messages.success(request, 'Xác thực email thành công.')
                    return redirect(request.GET.get('next') or '/')
            else:
                messages.error(request, 'Vui lòng nhập đúng mã xác thực')
    return render(request, 'pages/verification_email.html')


@login_required
def refresh_verification_code(request):
    user = request.user
    verification_code, created = VerificationCode.objects.get_or_create(user=user, is_verified=False)
    if not created and verification_code.is_code_expired():
        verification_code.create_verification_code()
    elif not created:
        verification_code.send_verification_email() 
    return JsonResponse({'message': 'Mã xác thực đã được làm mới và gửi lại email.'}, status=200)