from csv import list_dialects
from django.contrib import admin
from kookooleShop.models import CategoriesRoot
from kookooleShop.models import Categories
from kookooleShop.models import Product
from kookooleShop.models import CustomerPin
from kookooleShop.models import CustomerLogUp
from kookooleShop.models import Order


class AdminCategoriesRoot(admin.ModelAdmin):
    list_display =['name','image']
class AdminCategories(admin.ModelAdmin):
    list_display =['name','root_category','image']


class AdminProduct(admin.ModelAdmin):
    list_display =['name','price','category','description','image']




class AdminCustomerLogUp(admin.ModelAdmin):
     list_display =['verify','first_name','last_name','email','phone','pin','address','token']
     search_fields=['email']



class AdminOrder(admin.ModelAdmin):
   list_display=['cancelation','customer','product' ,'price','stock','quantity','qnty_price','time','address','phone','status']
   search_fields=['phone']
   

# Register your models here.
admin.site.register(CategoriesRoot ,AdminCategoriesRoot)
admin.site.register(Categories ,AdminCategories)
admin.site.register(Product ,AdminProduct)
admin.site.register(CustomerLogUp ,AdminCustomerLogUp)
admin.site.register(Order ,AdminOrder)
admin.site.register(CustomerPin)