from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
  def create_user(self, email, name, password=None, user_type="vendor"):
    if not email:
        raise ValueError("Users must have an email address")
    email = self.normalize_email(email)
    user = self.model(email=email, name=name, user_type=user_type)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, name, password):
    user = self.create_user(email, name, password, user_type="admin")
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser, PermissionsMixin):
  USER_TYPES = (
        ("admin", "Admin"),
        ("vendor", "Vendor"),
        ("customer", "Customer"),
    )
  
  email = models.EmailField(unique=True)
  name = models.CharField(max_length=255)
  user_type = models.CharField(max_length=10, choices=USER_TYPES, default="vendor")

  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["name", "password"]

  def __str__(self):
        return self.email