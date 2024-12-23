from django import forms
from django.core.validators import RegexValidator,EmailValidator,MinLengthValidator


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'block px-2.5 pb-2.5 pt-5 w-full text-sm text-zinc-900 bg-transparent rounded-xl border border-zinc-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
            'id': 'username',
            'required': True,
        }),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Tên đăng nhập không hợp lệ',
            ),
        ]
    )
    email = forms.EmailField(
        max_length=264,
        widget=forms.EmailInput(attrs={
            'class': 'block px-2.5 pb-2.5 pt-5 w-full text-sm text-zinc-900 bg-transparent rounded-xl border border-zinc-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
            'id': 'email',
            'required': True,
        }),
        validators=[
            EmailValidator(
                message='Email không hợp lệ',
            ),
        ]
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block px-2.5 pb-2.5 pt-5 w-full text-sm text-zinc-900 bg-transparent rounded-xl border border-zinc-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
            'id': 'phone_number',
            'required': True,
        }),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Số điện thoại không hợp lệ',
            ),
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block pl-2.5 pr-16 pb-2.5 pt-5 w-full text-sm text-zinc-900 bg-transparent rounded-xl border border-zinc-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
            ':type': "show ? 'text' : 'password'",
            'x-model':"value",
            'id': 'password',
            'required': True,
        }),
        validators=[
            MinLengthValidator(6,message='Mật khẩu phải có ít nhất 6 ký tự'),
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block pl-2.5 pr-16 pb-2.5 pt-5 w-full text-sm text-zinc-900 bg-transparent rounded-xl border border-zinc-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
            ':type': "show ? 'text' : 'password'",
            'x-model':"value",
            'id': 'confirm_password',
            'required': True,
        }),
        validators=[
            MinLengthValidator(6,message='Mật khẩu phải có ít nhất 6 ký tự'),
        ]
    )


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        if password != confirm_password:
            self.add_error('confirm_password', 'Mật khẩu không khớp')
        # Kiểm tra email không trùng lặp
        # if email:
        #     if User.objects.filter(email=email).exists():
        #         self.add_error('email', 'Email đã được sử dụng')
                
        return cleaned_data
