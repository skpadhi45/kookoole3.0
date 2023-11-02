 
from asyncio.windows_events import NULL
from email.policy import default
from pickle import TRUE
from django.db import models
import datetime
from django.db.models import Sum
 
 
# Create your models here.
class CategoriesRoot(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='media/')


    @staticmethod
    def  get_all_categoriesroot():

        return CategoriesRoot.objects.all()

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='media/')
    root_category= models.ForeignKey(CategoriesRoot , on_delete=models.CASCADE )

     

   

    


    #getting all product from Category model in get_all_products which is used in view.py
    @staticmethod
    def get_all_categories():

        return Categories.objects.all()

    #it will show name instead of showing oject name in admin page
    def __str__(self):
        return self.name

     

class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Categories , on_delete=models.CASCADE , default=1)
    stock = models.IntegerField(default=0)
    description = models.CharField(max_length=200 , default='')
    image = models.ImageField(upload_to='media/')
    root_category= models.ForeignKey(CategoriesRoot , on_delete=models.CASCADE ,default=1 )

    #it will show name instead of showing oject name in admin page
    def __str__(self):
        return self.name


#all products id in session cart .this is used in shopage view on buttom lines
    @staticmethod
    def get_products_by_id(ids):

        return Product.objects.filter(id__in =ids)


#getting all product from Product model in get_all_products which is used in view.py
    @staticmethod
    def get_all_products():

        return Product.objects.all()


#getting all product from Product model in get_all_products_by_category_id which is used in view.py
    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
  
           return Product.objects.filter(category = category_id)
        else:
           return Product.get_all_products();


class CustomerPin(models.Model):
    pin = models.CharField(max_length=10)
    post_name = models.CharField(max_length=50 , default='')

 #it will show name instead of showing oject name in admin page
    def __str__(self):
        return self.pin
 


class CustomerLogUp(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    token = models.CharField(max_length=150,default='')
    password_reset_token = models.CharField(max_length=150,default='')
    verify = models.BooleanField(default=False)
    password = models.CharField(max_length=500)
    phone = models.CharField(max_length=13 ,default='')
    address =models.CharField(max_length=200 , default='' ,blank=True)
    pin = models.CharField(max_length=10 ,default='')
    #profile_img=models.ImageField(upload_to='media/',default="kookoole.png",blank=True)
    profile_img=models.URLField(default="media/kookoole.png")

    
    def register(self):
        self.save()

     #it will show name instead of showing oject name in admin page
    def __str__(self):
        return self.email


     # filter email from from CustomerLogUp for log in comparision in view in homePage
    @staticmethod
    def get_customer_by_email(email):
        try:
            return CustomerLogUp.objects.get(email = email)
        except:
            return False
 
    def isExists(self):
         if CustomerLogUp.objects.filter(email = self.email):
             return True
          
         return False

    def isNotPinExists(self):
         if CustomerPin.objects.filter(pin = self.pin):
             return False
          
         return True


 

     



class Order(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE )
    customer = models.ForeignKey(CustomerLogUp , on_delete=models.CASCADE )
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    qnty_price= models.FloatField()
    address =models.CharField(max_length=200 , default='' ,blank=True)
    phone =models.CharField(max_length=20 , default='' ,blank=True)
    date = models.DateField(default=datetime.datetime.now)
    time =models.DateTimeField(auto_now=True)
    status = models.BooleanField(default = False)
    cancelation = models.BooleanField(default = True)
    stock = models.IntegerField(default=0)



    def placeOrder(self):
        self.save()


         #it will show name instead of showing oject name in admin page
    def __str__(self):
        return self.phone

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')

     
    def get_products_email_record(customer_id,n):
        

        return Order.objects.filter( customer =customer_id).order_by('-id')[:n]


    def get_total_price(customer_id,n):
      
        return Order.objects.filter( customer =customer_id).order_by('-id')[:n].aggregate(Sum('qnty_price'))

    #class Employee(models.Model):
         #first_name = models.CharField(max_length=50, null=False)
         #last_name = models.CharField(max_length=50) 
         #dept = models.ForeignKey( Department , on_delete=models.CASCADE , default=1)
class ContactUs(models.Model):
    
    email = models.EmailField()
     
    phone = models.CharField(max_length=13 ,default='')
    address =models.CharField(max_length=200 , default='' ,blank=True)
      
    
    location=models.URLField(default="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d7660527.340719109!2d85.82489999999999!3d20.362600000000008!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sin!4v1695367904279!5m2!1sen!2sin")