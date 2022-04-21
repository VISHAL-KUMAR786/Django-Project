from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name  = models.CharField(max_length=255)
    category = models.CharField(max_length=50,default="")
    subCategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=2000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to = 'shop/images',default="")


    def __str__(self) -> str:
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=100)
    email = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=50,default="")
    desc = models.CharField(max_length=2000,default="")

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name  = models.CharField(max_length=255)
    email = models.CharField(max_length=320 )
    address1 = models.CharField(max_length=2000)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)

    pass 

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField( auto_now_add=True)

    def __str__(self) -> str:
        return self.update_desc[:23] + '...'
    pass  