  
from django import template



register = template.Library()

#fileter for items exists in cart or not if exists return true else false 
@register.filter(name = 'multiply')
def multiply(number , number1):
    return number*number1
   
    