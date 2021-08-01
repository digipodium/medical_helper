from django.core.checks import messages
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.fields import CharField, DateTimeField, EmailField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator


#Create your models here.

duration_option =  (
    ('1','1-Day'),
    ('2', '2-Day'),
    ('3', '3-Day'),
    ('4', '4-Day'),
    ('5', '5-Day'),
    ('6', '6-Day'),
    ('7', '7-Day'),
    ('8', '8-Day'),
    ('9', '9-Day'),
    ('10', '10-Day'),
)
age_option = (
    ('grp0', ' new born babies < 12 months'),
    ('grp1', '1 to 10 yrs'),
    ('grp2', '11 to 20 yrs'),
    ('grp3', '21 to 30 yrs'),
    ('grp4', '31 to 40 yrs'),
    ('grp5', '41 to 60 yrs'),
    ('grp6', '60+'),

)
gender_option = (
    ('M', 'Male'),
    ('F', 'Female')
)



phone_regex = RegexValidator(regex=r'^\d{10,15}$', message="Phone number must be entered''''[['[]]] in the format: '999999999'. Up to 15 digits allowed.")


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    Full_Name = models.CharField(max_length=30, default='')
    gender = models.CharField(max_length=6,choices=gender_option, default='')
    email = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15,validators=[phone_regex], default='')
    pic = models.ImageField(upload_to='users')
    update_on = models.DateTimeField(auto_now=True)
    address=models.TextField(default="not available")

    def __str__(self):
        return self.user.username

class Equipment(models.Model):
    name = models.CharField(max_length=50)
    catagory = models.CharField(max_length=50, default='Machine_one')
    price = models.IntegerField(null=True)
    rent_price = models.IntegerField(null=True)
    image =  models.ImageField(upload_to='equipments')
    image_2 =  models.ImageField(upload_to='equipments')
    Description = models.TextField()
    availability = models.BooleanField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EquipmentRental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
    rent_price = models.IntegerField(null=True)
    rent_date = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(auto_now=True)
    Delivery_Address = models.TextField(max_length=500)
    is_date_expired = models.BooleanField(default=True)
    Fine = models.IntegerField(null=True)

    def __str__(self):
        return self.user

class Human_Resource(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField(null=True)
    address = models.TextField(max_length=500)
    helpertype = models.CharField(max_length=32)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=15,validators=[phone_regex])
    email = models.EmailField(blank=True)
    date_added = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField()
    img = models.ImageField(upload_to = "hr/",default="default_hr.jpg")
    experience = models.IntegerField(default=1)
    

    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    equipment = models.ForeignKey(Equipment,on_delete=models.DO_NOTHING)
    price = models.IntegerField(null=True)
    is_payment_complete = models.BooleanField()
    date_purchase = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to = "pc/",default="default_pc.jpg")

    def __str__(self):
        return self.user

class ServiceRequest(models.Model):
    hr = models.ForeignKey(Human_Resource, on_delete=models.CASCADE,related_name='hr_person')
    for_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='client')
    durations = models.CharField(max_length=100, choices=duration_option)
    gender = models.CharField(max_length=6, choices=gender_option,default='')
    age = models.CharField(max_length=30, choices=age_option,default='')
    request_for = models.TextField(default='')
    service_is_complete = models.BooleanField(default='True')
    
    class Meta:
        verbose_name = 'Patient detail'
        verbose_name_plural = 'Patient details'

    def __str__(self):
        return f'request from user:{self.for_user.username} for => helper: {self.hr.name}'

class Report(models.Model):
    class Feedback_options(models.TextChoices):
        COMPLAIN='CMP',_('complain')
        REVIEW='REV',_('review')
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    feedbackfor = models.CharField(max_length=15, choices=Feedback_options.choices,default=Feedback_options.REVIEW)
    message = models.CharField(max_length=100,)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],help_text="give a rating between 1 to 5")

class Contact(models.Model):
    """Model definition for Contact."""

    name = CharField(max_length=30)
    email =EmailField()
    subject = CharField(max_length=255)
    messages = TextField()
    
    class Meta:
        """Meta definition for Contact."""
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name


class Order(models.Model):
    class StatusOfOrder(models.TextChoices):
        PROCESSING = 'P',_('Processing')
        TRANSIT = 'T',_('In Transit')
        DELIVERED = 'D',_('delivered')
        CANCELLED = 'C',_('cancelled')
       

    buyer = ForeignKey(User,on_delete=DO_NOTHING)
    product = ForeignKey(Equipment,on_delete=DO_NOTHING)
    status = CharField(max_length=15,choices=StatusOfOrder.choices, default=StatusOfOrder.PROCESSING)
    date = DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.buyer.username} order {self.product.name} status : {self.status}'