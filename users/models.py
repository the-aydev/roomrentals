from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, number, email=None, full_name=None, photo=None, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        # email = self.normalize_email(email)
        # email = email.lower()

        user = self.model(
            number=number,
            full_name=full_name,
            email=self.normalize_email(email),
            photo=photo,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, number, email=None, full_name=None, photo=None, password=None):
        user = self.create_user(
            number, email=email, full_name=full_name, photo=photo, password=password)

        user.staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, number, email=None, full_name=None, photo=None, password=None):
        user = self.create_user(
            number, email=email, full_name=full_name, photo=photo, password=password)

        user.admin = True
        user.staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=False, null=False)
    number = models.CharField(max_length=15, unique=True,)
    photo = models.ImageField(blank=True, null=True,
                              upload_to='users/profile_picture')
    timestamp = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['full_name', 'email']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    objects = UserManager()

    def __str__(self):
        return self.number
