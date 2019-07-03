from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



class User_manager(BaseUserManager):

    #method to create a basic user
    def create_user(self, username, first_name, last_name, email, phone, housenumber, locality, village, mandal, district, pincode, password):
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            housenumber = housenumber,
            locality = locality,
            village = village,
            mandal = mandal,
            district = district,
            pincode = pincode,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    #different method for creation of a superuser. Very few fields to be entered comparatively
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            first_name = "Default",
            last_name = "Superuser",
            email = email,
            phone = "Null",
            housenumber = "Null",
            locality = "Null",
            village = "Null",
            mandal = "Null",
            district = "Null",
            pincode = "Null",
            password = password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(PermissionsMixin, AbstractBaseUser):

#All the fields that every user will have
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=32, unique=True)
    phone = models.CharField(max_length=10)
    housenumber = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    mandal = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #For user creation through terminal
    REQUIRED_FIELDS = ["email"]

    #Username will be used as username field
    USERNAME_FIELD = "username"

    #calling User_manager class
    objects = User_manager()

    #User object can be referenced by string username
    def __str__(self):
        return self.username

    #Additional permissions that a user caan have
    class Meta:
            permissions = (("can view dashboard","To open dashboard"),
                ("can view manager level","To open manager dashboard"),
                ("can view staff dashboard","To open staff dashboard"))


#Creating new group objects
p, created = Group.objects.get_or_create(name='staff')
p, created = Group.objects.get_or_create(name='manager')
p, created = Group.objects.get_or_create(name='supportstaff')
