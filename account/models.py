from django.db import models

# Create your models here.
# create a custom models using abstract user class or abstract base class, abstrat user class allows us to add ontop of what the django built in models already have, to build your own user model class to build our own custom user model we use the abstract base class, because we want to build from scratch

# create out abstract base class
# PermissionMixin Add the fields and methods necessary to support the Group and Permission models using the ModelBackend.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
# to set token manually
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    # auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get('email'))
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def _str_(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
# otp model
class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    
    def _str_(self):
        return f'{self.user.first_name} passcode'