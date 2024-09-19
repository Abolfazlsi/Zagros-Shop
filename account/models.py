from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an phone")

        user = self.model(
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="ادرس ایمیل",
        max_length=255,
        null=True,
        blank=True,
        unique=True,

    )
    fullname = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی", null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن", null=True)
    profile_image = models.ImageField(upload_to="profile_image", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = "phone"

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"

    def __str__(self):
        if self.phone:
            return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=90)
    address = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    postal_code = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.phone} - {self.address}"

    class Meta:
        verbose_name = "ادرس"
        verbose_name_plural = "ادرس ها"
