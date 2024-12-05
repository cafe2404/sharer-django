from django.db import models
from django.utils import timezone

# Create your models here.
class Platform(models.Model):
    class NameChoice(models.TextChoices):
        SEMRUSH = 'Semrush'
        KEYWORDS_TOOL = 'Keywords Tool'
        CANVA = 'Canva'
        FREEPiK = 'FreePik'
        MINEA = 'Minea'
        PLACE_IT = 'Placeit'
        PIPI_ADS = 'Pipi Ads'
        HEY_ESTY = 'Heyesty'
        DROPSHIP = 'Dropship'
        AUTO_DS = 'Auto DS'
        
    name = models.CharField(max_length=100, choices=NameChoice.choices,default=NameChoice.SEMRUSH)
    description = models.TextField()
    url = models.URLField()
    logo_url = models.URLField()
    css_text = models.TextField(blank=True,null=True)
    js_script = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    def to_dict(self):
        return {
            "name":self.name,
            'url':self.url,
            'logo_url':self.logo_url,
            'description':self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
class PlatformAccount(models.Model):
    class LoginChoice(models.TextChoices):
        USERNAME_PASSWORD = 'Username/Password'
        COOKIE = 'Cookie'
    login_method = models.CharField(max_length=100, choices=LoginChoice.choices,default=LoginChoice.USERNAME_PASSWORD)
    platform     = models.ForeignKey(Platform, on_delete=models.CASCADE)
    username     = models.CharField(max_length=100)
    password     = models.CharField(max_length=100)
    cookie       = models.TextField()
    login        = models.TextField(choices=LoginChoice.choices,default=LoginChoice.USERNAME_PASSWORD,blank=True,null=True,verbose_name='Đăng nhập bằng')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    expired_at   = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    def to_dict(self):
        data = {
            'id': self.id,
            'platform': self.platform.to_dict(),
            'login': self.login,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'expired_at': self.expired_at,
        }
        if self.login == 'Cookie':
            data['cookie'] = self.cookie
        else:
            data['username'] = self.username
            data['password'] = self.password
        # Thêm thời gian còn lại vào dict nếu có
        data['time_left'] = self.time_left()
        if data['time_left']['string'] ==  'Hết hạn':
            return {
                'platform': self.platform.to_dict(),
                'time_left': {
                    'string': 'Hết hạn',
                }
            }
        return data
    def time_left(self):
        if self.expired_at:
            now = timezone.now()
            # Tính sự khác biệt giữa expired_at và thời gian hiện tại
            time_left = self.expired_at - now
            
            # Tính ngày, giờ, phút từ timedelta
            days = time_left.days
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            if time_left.total_seconds() < 0:
                return {'string': 'Hết hạn'}
        
            return {
                'days': days,
                'hours': hours,
                'minutes': minutes,
                'string': f'Còn lại {days} ngày {hours} giờ {minutes} phút',
            }
        else:
            return {
                'days': None,
                'hours': None,
                'minutes': None,
                'string': 'Vĩnh viễn',
            }
    def __str__(self):
        return self.username