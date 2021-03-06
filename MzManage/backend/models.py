from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser
)

# Create your models here.

"""
class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email,password)
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name = 'email address',
        max_length = 255,
        unique = True,
        db_index=True
    )
    username = models.CharField(max_length=255,
                                unique=True,
                                db_index=True,
                                blank=True
                               )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(('last login'), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        username,_ = self.email.strip().split("@")
        return username.replace('.','_')
    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
"""
