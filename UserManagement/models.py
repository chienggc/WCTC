from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    product_category= models.CharField(max_length=20, blank=False, null=True, unique=True)
    category_desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product_category

class Product(models.Model):
    prd_name = models.CharField('Product Name', max_length=100, unique=True)
    prd_desc = models.TextField('Product Description', blank=True)
    price = models.IntegerField()
    product_category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.CASCADE)
    product_image = models.ImageField(null=True, blank=True, upload_to="images/")

    # picture= models.UR

    def __str__(self):
        return self.prd_name

class Redemption(models.Model):
    redeemer = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, related_name='redeemer')
    gift = models.ForeignKey(Product, blank=False, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    updated_date = models.DateTimeField('Updated Date')
    acknowledgeby = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='acknowledgeby')

    def __str__(self):
        return self.redeemer.username + self.gift.prd_name

class PointLog(models.Model):
    previous_point = models.IntegerField(default=0)
    latest_point = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    point_date = models.DateTimeField('Point Date')
    action = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id.username + " " + self.action + " Point: " + str(self.latest_point) + " AT: " + str(self.point_date)
