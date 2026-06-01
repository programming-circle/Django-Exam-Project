from django.db import models
import uuid #guid
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils.text import slugify
from django.conf import settings

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
    model_name = models.CharField(max_length=255, verbose_name="Model Name")
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
    image_path = models.CharField(max_length=255, null=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name="Stok Quantity")
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
    
