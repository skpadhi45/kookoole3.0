from django import template



register = template.Library()

#fileter for items exists in cart or not if exists return true else false 
@register.filter(name = 'is_in_cart')
def is_in_cart(product ,cart):
   
   keys = cart.keys()
   for id in keys:
       #print(id , product.id)
       #print(type(id) , type(product.id))
       if int(id) == product.id:
           return True
 
   return False;


#fileter for counting quantity cart item
@register.filter(name = 'cart_quantity')
def cart_quantity(product ,cart):
   keys = cart.keys()
   for id in keys:
       
       if int(id) == product.id:
           return cart.get(id)
 
   return 0;

#total price of single product with quantity wise in cart page
@register.filter(name = 'total_price')
def  total_price(product ,cart):
    if product.stock<=0:
      return 0* product.price * cart_quantity(product , cart)
    else:
      return product.price * cart_quantity(product , cart)

 


#total price of all products with quantity wise in cart page
@register.filter(name = 'total_cart_price')
def  total_cart_price(s_products ,cart):
     sum =0 ;
     for product in s_products :
         sum += total_price(product, cart)
  
     return sum
#total price of all products with quantity wise in cart page
@register.filter(name = 'total_cart_price_includding_delevery_charges')
def  total_cart_price(s_products ,cart):
     sum =35 ;
     for product in s_products :
         sum += total_price(product, cart)
  
     return sum
