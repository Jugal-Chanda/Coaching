from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUserManager(BaseUserManager):
    """custom user manager class"""
    use_in_migration = True

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

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_student',True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superadmin', True)

        if extra_fields.get('is_superadmin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Batch(models.Model):
    """docstring for ."""
    name = models.CharField(max_length=50, blank=False)
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    enrolled = models.IntegerField(default = 0)
    created_at = models.DateField(auto_now=True)
    REQUIRED_FIELDS = ['name','capacity']

    def __str__(self):
        return self.name



class User(AbstractBaseUser):
    """ Custom user model class"""
    email = models.EmailField(_('email'), unique=True, default='')
    name = models.CharField(_('name'), max_length=50, blank=False)
    image = models.ImageField(upload_to="accounts/")
    phone_number = models.CharField(max_length = 15)
    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    teacher_aprove = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    student_aprove = models.BooleanField(default=False)
    address = models.CharField(max_length=255,blank=False,default="")
    payment = models.BooleanField(default = False)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone_number','image','address']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.email
