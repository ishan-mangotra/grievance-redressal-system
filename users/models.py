from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from multiselectfield import MultiSelectField



m1="Mee Seva"
m2="T-App"
m3="T-Wallet"
m4="Citizen"
mode_choice = ((m1,"Mee Seva"),(m2,"T-App"),(m3,"T-Wallet"),(m4,"Citizen"))

c1="Revenue"
c2="Food and Civil Supplies"
c3="GHMC"
c4="Commercial Taxes"
c5="SPDCL"
c6="NPDCL"
c7="Others"
c8="Citizen"
category_choice = (
    (c1,"Revenue"),
    (c2,"Food and Civil Supplies"),
    (c3,"GHMC"),
    (c4,"Commercial Taxes"),
    (c5,"SPDCL"),
    (c6,"NPDCL"),
    (c7,"Others"),
    (c8,"Citizen")
)

class User_manager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, phone, housenumber, locality, village, mandal, district, pincode, password, mode, category):
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
            mode = m4,
            category = c8
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

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
            category = c8,
            mode = m4,
            password = password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(PermissionsMixin, AbstractBaseUser):

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
    mode = MultiSelectField(max_length = 255, choices=mode_choice, default = mode_choice[3][0])
    category = MultiSelectField(max_length = 255, choices=category_choice, default = category_choice[7][0])


#    gender_choices = [("M", "Male"), ("F", "Female"), ("O", "Others")]
#    gender = models.CharField(choices=gender_choices, default="M", max_length=1)
#    nickname = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"
    objects = User_manager()

    def __str__(self):
        return self.username

    class Meta:
        permissions = (("can view dashboard","To open dashboard"),
            ("can view manager level","To open manager dashboard"),
            ("can view staff dashboard","To open staff dashboard"))

p, created = Group.objects.get_or_create(name='staff')
p, created = Group.objects.get_or_create(name='manager')
p, created = Group.objects.get_or_create(name='supportstaff')
