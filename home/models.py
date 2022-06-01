from django.db import models
from datetime import datetime
from .validators import validate_file_extension

# Create your models here.
itemcategory=[('bread','bread'),('cakes','cakes'),('pastries','pastries'),('cookies','cookies')]
itemsubcategory=[("white","white"),("bagel","bagel"),("whole wheat","whole wheat"),("sourdough","sourdough"),("rye","rye"),("multigrain","multigrain"),("eggdough","eggdough")]
class Product(models.Model):
    category=models.CharField(choices=itemcategory,max_length=200,blank=True)
    subcategory=models.CharField(choices=itemsubcategory,max_length=200,blank=True)
    product_name= models.CharField(null=False,max_length=200)
    price = models.FloatField(blank=False,null=False)
    discount_price=models.FloatField()
    image= models.FileField(upload_to='images/',blank=False, validators=[validate_file_extension])

class Blog(models.Model):
    title=models.CharField(blank=False,null=False,max_length=200)
    subtitle=models.CharField(blank=False,null=False,max_length=200)
    image= models.FileField(upload_to='images/',blank=False, validators=[validate_file_extension])
    content = models.TextField(blank=False,null=False)
    timestamp=models.DateTimeField(blank=False,null=False)
    author = models.TextField(blank=False,null=False)

class About(models.Model):
    heading=models.CharField(blank=False,null=False,max_length=200)
    subheading=models.CharField(max_length=200,blank=True)
    content = models.TextField(blank=False,null=False)
    author = models.TextField(blank=False,null=False)
    footnote=models.CharField(blank=False,null=False,max_length=200)

class orderitem(models.Model):
    customer =models.CharField(max_length=50)
    product =models.CharField(max_length=2000)
    price=models.IntegerField(default=0)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    date=models.DateField(default=datetime.now)
    orderstatus=models.CharField(max_length=50,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=50,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=50,null=True,blank=True)
    razorpay_signature=models.CharField(max_length=50,null=True,blank=True)

    def placeorder(self):
        self.save()
