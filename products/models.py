from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    add_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="category_add_by")
    add_date = models.DateTimeField(default=datetime.today())
    del_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="category_del_by", null=True, blank=True)
    del_date = models.DateTimeField(default=datetime.today())
    modify_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="category_modify_by", null=True,
                                  blank=True)
    modify_date = models.DateTimeField(default=datetime.today())
    is_del = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Products(models.Model):
    user_id = models.ForeignKey(User, related_name="product_user_id", on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name="product_category", on_delete=models.PROTECT)
    product_name = models.CharField(max_length=500)
    product_code = models.CharField(max_length=500)
    price = models.FloatField(default=0)
    manufacturing_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    add_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="product_add_by")
    add_date = models.DateTimeField(default=datetime.today())
    del_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="product_del_by", null=True, blank=True)
    is_del = models.BooleanField(default=False)
    del_date = models.DateTimeField(default=datetime.today())
    modify_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="product_modify_by", null=True,
                                  blank=True)
    modify_date = models.DateTimeField(default=datetime.today())

    def __str__(self):
        return self.product_name + self.product_code
