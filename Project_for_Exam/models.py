from django.db import models
import uuid #guid
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils.text import slugify
from django.conf import settings

#Autorization libraries: 
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin

class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="Brand Name")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        db_table = 'dj_brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

class Cars(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    # model_name = models.CharField(max_length=255, verbose_name="Model Name")
    slug = models.SlugField()
    description = models.TextField(null=False, verbose_name="Product Description")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        null=True,
        blank=True,
        verbose_name='Discount Price'
    )

    brand = models.ForeignKey(
        Brand, 
        on_delete=models.CASCADE, 
        related_name='cars', 
        verbose_name="Car Brand"
    )

    is_active = models.BooleanField(default=True)
    image_path = models.ImageField(upload_to='assets/', null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0, blank=True, verbose_name="Stock Quantity")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def get_final_price(self):
        if self.discount_price is not None and self .discount_price < self.price:
            return self.discount_price
        return self.price
    
    class Meta:
        db_table = 'cars_product'
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f"""
        '''''''''''''''''''''''''''''''''''''''''''''''''''''
        ProductId: {self.id}
        Name: {self.name}
        Price: {self.price}
        Description: {self.description}
        '''''''''''''''''''''''''''''''''''''''''''''''''''''
        """
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_ID = models.UUIDField(primary_key=False, default=uuid.uuid4,editable=False)
    car = models.ForeignKey(
        Cars, 
        on_delete=models.CASCADE, 
        related_name='cars', 
        verbose_name="Car"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) #when car order creating
    closed_at = models.DateTimeField(auto_now=True) #when car order finished by buying or declaying
    # just for getting price of Car
    def get_price(self):
        if self.car is not None and self.car.price is not None:
            return None
        return self.car.price
    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    def __str__(self):
        return f"""
        '''''''''''''''''''''''''''''''''''''''''''''''''''''
        ProductId: {self.id}
        Car: {self.car}
        Active status: {self.is_active}
        Date of order: {self.created_at}
        Date of finish order: {self.closed_at}
        '''''''''''''''''''''''''''''''''''''''''''''''''''''
        """

    
# Custom admin panel \ autorization system block

#user managing. 
class MyUserManager(BaseUserManager):
    # C operation for usual User
    def create_user(self,email,password, **extra_fields):
        email= self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # C oper for super User (admin)
    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
# Main class for user that could be or User or Stuff cause of "is_staff"&"is_superuser"  varuable
class MyUser(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    Birth_date = models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name",]

    objects = MyUserManager()

    def __str__(self):
        return self.email