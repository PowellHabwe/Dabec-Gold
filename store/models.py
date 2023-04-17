from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price =  models.FloatField()
    price_original =  models.FloatField(null=True)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    purity = models.IntegerField()
    is_available = models.BooleanField(default = True)
    home_bar = models.BooleanField(default = False)
    home_coin = models.BooleanField(default = False)
    home_nugget = models.BooleanField(default = False)
    home_ornament = models.BooleanField(default = False)
    affordable = models.BooleanField(default = False)
    top_rated = models.BooleanField(default = False)
    new = models.BooleanField(default = False)
    best_sellers = models.BooleanField(default = False)
    deals = models.BooleanField(default = False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name