from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import CustomUser as User, VerificationCode, UserSession
from django.http import JsonResponse
from ..forms  import SignupForm
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from ..decorators import verification_required
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            device_uuid = request.COOKIES.get('device_uuid') or str(uuid.uuid4())
            # Kiểm tra trạng thái đăng nhập
            try:
                session = UserSession.objects.get(user=user)
                if session.is_active and session.device_uuid != device_uuid:
                    messages.error(request, "Bạn đã đăng nhập trên một thiết bị khác.")
                    return render(request, 'pages/login.html')

                session.device_uuid = device_uuid
                session.is_active = True
                session.save()
            except UserSession.DoesNotExist:
                UserSession.objects.create(user=user, device_uuid=device_uuid, is_active=True)

            login(request, user)
            response = redirect(request.GET.get('next') or '/')
            response.set_cookie('device_uuid', device_uuid, httponly=True)
            
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            
            return response
        messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
    return render(request, 'pages/login.html')


def logout_view(request):
    try:
        session = UserSession.objects.get(user=request.user)
        session.is_active = False
        session.save()
    except UserSession.DoesNotExist:
        pass
    logout(request)
    response = redirect('/login')
    response.delete_cookie('device_uuid')
    return response


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
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            
            url = reverse('verification_email')
            # messages.success(request, 'Kiểm tra email của bạn để xác thực')
            url += f'?next={request.GET.get("next") or '/'}'
            return redirect(url)
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
    
    verification_code = VerificationCode.create_or_reset_verification_code(user)
    
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
                    return redirect(request.GET.get('next') or '/')
            else:
                messages.error(request, 'Vui lòng nhập đúng mã xác thực')
    return render(request, 'pages/verification_email.html')


@login_required
def refresh_verification_code(request):
    user = request.user
    verification_code, created = VerificationCode.objects.get_or_create(user=user, is_verified=False)
    if not created:
        verification_code.reset_verification_code()
        verification_code.send_verification_email()
    else:
        verification_code.send_verification_email() 
    return JsonResponse({'message': 'Mã xác thực đã được làm mới và gửi lại email.'}, status=200)


@login_required
def change_email_view(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        user = request.user
        if VerificationCode.objects.filter(user__email=new_email,is_verified=True).exists():
            messages.error(request, 'Email đã được xác thực ở một tài khoản khác.')
        elif new_email == user.email:
            messages.error(request, 'Email mới không được phép giống với email hiện tại.')
        else:
            user.email = new_email
            user.save()
            verification_code = VerificationCode.objects.get(user=user) 
            if verification_code:
                verification_code.delete()
            messages.success(request, 'Vui lòng xác thực email.')
            return redirect('verification_email',next=request.GET.get('next') or '/')
    return render(request, 'pages/change_email.html')

@login_required
@verification_required
def authentication_extension_view(request):
    access_token = request.session['access_token']
    refresh_token = request.session['refresh_token']
    
    return render(request, 'pages/authentication_extension.html',{
        'access_token': access_token,
        'refresh_token': refresh_token,
    })