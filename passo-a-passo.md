# django-custom-login-email


### Instale as dependências

```
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install Django==3.1.8 dj-database-url django-extensions python-decouple

pip freeze | grep Django==3.1.8 >> requirements.txt
pip freeze | grep dj-database-url >> requirements.txt
pip freeze | grep django-extensions >> requirements.txt
pip freeze | grep python-decouple >> requirements.txt

cat requirements.txt
```


### Criando um .gitignore

Veja no repositório do projeto.

https://github.com/rg3915/django-custom-login-email/blob/main/.gitignore

### Gere um arquivo .env

Copiar o conteúdo de `env_gen.py`

https://github.com/rg3915/django-custom-login-email/blob/main/contrib/env_gen.py

```
mkdir contrib
touch contrib/env_gen.py

python contrib/env_gen.py

cat .env
```


### Criando um projeto

```
django-admin.py startproject myproject .
```

### Criando uma app

```
cd myproject
python ../manage.py startapp accounts
python ../manage.py startapp core
python ../manage.py startapp crm
```

#### Deletando alguns arquivos

```
rm -f core/admin.py
rm -f core/models.py
```

#### Criando alguns arquivos

```
touch accounts/managers.py
touch accounts/urls.py
touch core/urls.py
```

### Editar settings.py

```python
# settings.py
from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as dburl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

AUTH_USER_MODEL = 'accounts.User'

...

INSTALLED_APPS = [
    ...
    # thirty apps
    'django_extensions',
    # my apps
    'myproject.accounts',
    'myproject.core',
    'myproject.crm',
]

...

default_dburl = 'sqlite:///' + str(BASE_DIR / 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}

...

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

...

USE_THOUSAND_SEPARATOR = True

DECIMAL_SEPARATOR = ','

...

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = 'core:index'
# LOGOUT_REDIRECT_URL = 'core:index'
```

### Editar urls.py

```python
# urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('myproject.core.urls', namespace='core')),
    path('accounts/', include('myproject.accounts.urls')),  # without namespace
    path('admin/', admin.site.urls),
]
```

### Editar core/urls.py

```python
# core/urls.py
from django.urls import path

from myproject.core import views as v

app_name = 'core'


urlpatterns = [
    path('', v.index, name='index'),
]
```

### Editar core/views.py

```python
# core/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


# @login_required
def index(request):
    return HttpResponse('<h1>Django</h1><p>Página simples.</p>')
```

### Editar accounts/models.py

```python
# accounts/models.py
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
```

### Editar accounts/managers.py

```python
# accounts/managers.py
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
```

### Editar accounts/admin.py

```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_admin',
                # 'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
```

### Editar accounts/urls.py

```python
# accounts/urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

# Read https://github.com/rg3915/django-auth-tutorial

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
```

### Editar accounts/tests.py

```python
# accounts/tests.py
from django.test import TestCase

from myproject.accounts.models import User


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@email.com',
            password='demodemo',
            first_name='Admin',
            last_name='Admin',
        )
        self.superuser = User.objects.create_superuser(
            email='superadmin@email.com',
            password='demodemo'
        )

    def test_user_exists(self):
        self.assertTrue(self.user)

    def test_str(self):
        self.assertEqual(self.user.email, 'admin@email.com')

    def test_return_attributes(self):
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'is_admin',
            'is_superuser',
            'date_joined',
            'last_login',
        )

        for field in fields:
            with self.subTest():
                self.assertTrue(hasattr(User, field))

    def test_user_is_authenticated(self):
        self.assertTrue(self.user.is_authenticated)

    def test_user_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_user_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_user_is_superuser(self):
        self.assertFalse(self.user.is_superuser)

    def test_superuser_is_superuser(self):
        self.assertTrue(self.superuser.is_superuser)

    def test_user_has_perm(self):
        self.assertTrue(self.user.has_perm)

    def test_user_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms)

    def test_user_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'Admin Admin')

    def test_user_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'Admin')
```

### Editar crm/models.py

```python
# crm/models.py
from django.conf import settings
from django.db import models


class Phone(models.Model):
    phone = models.CharField(max_length=13)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # noqa E501

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'telefone'
        verbose_name_plural = 'telefones'

    def __str__(self):
        return self.user.email
```

### Editar crm/admin.py

```python
# crm/admin.py
from django.contrib import admin

from .models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone')
    search_fields = ('user__email',)
```

### Editar crm/tests.py

```python
# crm/tests.py
from django.test import TestCase

from myproject.accounts.models import User
from myproject.crm.models import Phone


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@email.com',
            password='demodemo',
            first_name='Admin',
            last_name='Admin',
        )
        self.phone = Phone.objects.create(
            phone='9876-54321',
            user=self.user
        )

    def test_phone_exists(self):
        self.assertTrue(self.phone)

    def test_str(self):
        self.assertEqual(self.user.email, 'admin@email.com')
```




```
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser --email='admin@email.com'

python manage.py test
```
