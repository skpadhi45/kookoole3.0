 
 
from ast import Import
import email
from email.mime import image
from multiprocessing import Value
from optparse import Values
from os import name
from pickle import NONE
from types import NoneType
from django.http import HttpResponse
from django.shortcuts import render ,redirect
from django.contrib.auth.hashers import make_password , check_password
from kookooleShop.models import Product
from kookooleShop.models import Categories
from kookooleShop.models import CategoriesRoot

from kookooleShop.models import CustomerPin
from kookooleShop.models import CustomerLogUp
from kookooleShop.models import Order
from kookooleShop.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
import uuid
from django.core.files.storage import FileSystemStorage


        
  

def shopPage(request):
#methods manage ment
 post=request.method =='POST'
 get=request.method =='GET'
  
 if  get:
    n=[]#this varible is used for showing data rootcategory -category-product in this maner 
    customer_first_name=None
    customer_last_name=None
    customer_phone=None
    customer_img=None
    customer_verify=None
    #for user profile
    customer = request.session.get('email')
    customer_dtls=CustomerLogUp.objects.filter(email=customer)
    for i in customer_dtls:
        customer_first_name=i.first_name
        customer_last_name=i.last_name
        customer_phone=i.phone
        customer_img=i.profile_img
        customer_verify=i.verify

    print(customer_first_name)
    print(customer_last_name)
    print(customer_phone)
    print(customer_img)
    
    #end user profile

    #if kooky deleted error handeled(if cart not exists it through error) creating empty cart to overcome the error
    cart = request.session.get('cart')
    if not cart:
        request.session['cart']={}
    # end 
    all_products = None
    sub_categories=None
    
    categoryrootID=request.GET.get('root_category')
    categoryID = request.GET.get('category')
    #print(sub_categories)
    all_categories_root=CategoriesRoot.get_all_categoriesroot()
    if categoryrootID:
        #sub_categories=Categories.objects.filter(root_category= categoryrootID)
        all_products = Product.objects.filter(root_category=categoryrootID)
        for i in all_products: 
            n.append(i.category_id)
        n =list(set(n))
        sub_categories=Categories.objects.filter(id__in=n)
         
        finaldata = all_products 
    #else:
        #sub_categories=Categories.objects.all()
     
    
    if categoryID :
        
        all_products = Product.get_all_products_by_category_id(categoryID);
        for i in all_products: 
            n.append(i.category_id)
        n =list(set(n))
        
        m=i.root_category_id
        #print(m)
        sub_categories=Categories.objects.filter(root_category_id=m)
         
        finaldata = all_products
            
            
        
        
    else:
        
        all_products = Product.objects.filter(root_category=categoryrootID)
        
        for i in all_products: 
            n.append(i.category_id)
        n =list(set(n))
        #sub_categories=Categories.objects.filter(id__in=n)
        #adding pagination
        paginator= Paginator(all_products, 18)
        page_number=request.GET.get('page')
        finaldata=paginator.get_page(page_number)
 
    if not categoryID and not categoryrootID:
        all_products = Product.get_all_products()
        for i in all_products: 
            n.append(i.category_id)
        n =list(set(n))
        sub_categories=Categories.objects.filter(id__in=n)
        paginator= Paginator(all_products, 6)
        page_number=request.GET.get('page')
        finaldata=paginator.get_page(page_number)
 
        

    data ={}
     
    data['products'] = finaldata
    #data['categories'] = all_categories
    data['categoriesroot'] = all_categories_root
    data['subcategories'] = sub_categories
    #for profile data
    data['customer_first_name'] = customer_first_name
    data['customer_last_name'] = customer_last_name
    data['customer'] = customer
    data['customer_phone'] = customer_phone
    data['customer_img'] = customer_img
    data['customer_verify']=customer_verify

    #end profile data
     
    
     
     
    #print('you are :',request.session.get('email'))
     

    return render(request,'shop.html' , data)


 if  post:
      
     error_massage= None
     id =request.POST.get('id')
     stock=request.POST.get('stock')
     qty=request.POST.get('qty')
     print(stock)
     categoryrootID=request.POST.get('rootcategoryid')
     categoryid=request.POST.get('categoryid')
     sub_categories=Categories.objects.filter(root_category_id=categoryrootID )
     #print(sub_categories)
     all_categories_root=CategoriesRoot.get_all_categoriesroot()
     #print(all_categories_root)
     cart = request.session.get('cart')
     all_categories = Categories.get_all_categories();
    
     categoryID = request.GET.get('category')
     if categoryrootID:
        all_products = Product.objects.filter(root_category_id=categoryrootID , category=categoryid)
        finaldata = all_products
        
     else:
         
        all_products = Product.objects.filter(root_category_id=categoryrootID )
     
     if cart:
         quantity = cart.get(id)
         if quantity:
             if 'minus' in request.POST:
                 if quantity<=1:
                     cart.pop(id)
                 else:
  
                   cart[id] =quantity-1

             

             elif 'plus' in request.POST:
                 if quantity >=int(stock):
                     error_massage="quantity not available"
                 else:
                   cart[id] = quantity+1
             elif 'qty' in request.POST:
                  
                   if int(qty) <=int(stock):
                      cart[id] =int(qty)
                   else:
                       error_massage="quantity not available"
         else:
             cart[id] = 1

     else:
         cart ={}
         cart[id] = 1

     request.session['cart'] = cart
     #print(request.session['cart'])
     
     
     data ={}
     
     data['products'] = finaldata 
     data['subcategories'] = sub_categories
     data['categoriesroot'] = all_categories_root
     
     return render(request,'shop.html' , data)
     #return redirect("/")

  
 
 
# handelling GET and POST method for signup page
def send_email_after_registration(email,token):
    subject ="Verify Email"
    message = f'Hi click on the link to verify your account http://127.0.0.1:8000/account_verify/{token}'
    from_email =settings.EMAIL_HOST_USER
    recipient_list =[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)


def signupPage(request):
 #methods manage ment
 post=request.method =='POST'
 get=request.method =='GET'
 
 if  get:


        return render(request,"signup.html")
 if post:
        postData = request.POST
        first_name = postData.get('Firstname')
        last_name =  postData.get('Lastname')
        email =  postData.get('Email')
        password = postData.get('Password')
        phone = postData.get('Phone')
        address = postData.get('paramanent_address')
        pin = postData.get('Pin')
        uid=uuid.uuid4()
        #print(uid)
 
        #to see the inserted value in text field we have to store value dictionary

        value ={
            'first_name':first_name ,
            'last_name'  :last_name ,
            'email' :email ,
            'phone' :phone ,
            'pin' :pin  ,
            'address' :address  ,
            'uid' :uid ,
            
            }
        

        error_message = None
        success_message=None 

        # loading data in customer oject it will be registered (stored) in data base
        customer = CustomerLogUp(first_name=first_name ,
                                 last_name=last_name ,
                                 email=email ,
                                 password=password, 
                                 phone=phone,
                                 address=address,
                                 pin=pin ,
                                 token=uid)



        #validatting(it is optional in sever side it can be validated in front end side also)

        if not first_name:
            error_message ="First Name Required !!!"
        elif len(first_name) < 1:
            error_message ="First Name Must Be 1 Char Long !!"


        elif not last_name:
            error_message ="Last Name Required !!!"
        elif len(last_name) < 2:
            error_message ="Last Name Must Be 2 Char Long !!"


        elif not email:
            error_message ="Email Required !!!"
        elif len(email) < 5:
            error_message ="Email Must Be 5 Char Long !!"
         

        # email already exist in data base true
        elif customer.isExists():
            error_message ="ଇମେଲ୍ ପୂର୍ବରୁ ବିଦ୍ୟମାନ ଅଛି । ଅନ୍ୟ ଇମେଲ୍ ID ବ୍ୟବହାର କରନ୍ତୁ !!"


        elif not password:
            error_message ="ପାସୱାର୍ଡ ଆବଶ୍ୟକ !!!"
        elif len(password) < 5:
            error_message ="ପାସୱାର୍ଡ ପାଞ୍ଚ ଅକ୍ଷର ହେବା ଜରୁରୀ  !!"

        
        elif not phone:
            error_message ="ଫୋନ୍ ନମ୍ଵର୍ ଆବଶ୍ୟକ !!!"
        elif len(phone) < 10:
            error_message ="ଫୋନ୍ ନମ୍ଵର୍ 10 ଅକ୍ଷର ହେବା ଆବଶ୍ୟକ !!"
        elif not address:
            error_message ="address ଆବଶ୍ୟକ !!!"

        elif not pin:
            error_message ="ପିନ୍ ଆବଶ୍ୟକ !!!"

        elif len(pin) != 6 : 
            error_message ="ପିନ୍ ଛଅ ଅକ୍ଷର ହେବା ଜରୁରୀ"

        #elif pin not in ['754109'] :
        elif customer.isNotPinExists():
            
            error_message ="ଆମେ ଏହି ସ୍ଥାନକୁ ସେବା ଦେଉନାହୁଁ"
            
 
        # loaded data in customer oject will be registered in data base

        if not error_message:
            customer.password =make_password(customer.password)#hashing password
 
           
            customer.register()#("cussessfuly registered in database") 
             
 
            #sending mail for verification calling send mail function


            send_email_after_registration(email,uid)
            #messages.success(request ,"Your Account Created Successfuly ,To Verify Your Account Check Your Email")
            success_message ="ଆପଣଙ୍କ ଆକାଉଣ୍ଟ ସଫଳତାର ସହ ସୃଷ୍ଟି ହୋଇଛି। ଆପଣଙ୍କ ଆକାଉଣ୍ଟ ଯାଞ୍ଚ କରିବାକୁ ଆମେ ଏକ ମେଲ୍ ପଠାଇଛୁ ଦୟାକରି ଆପଣଙ୍କ ଇନବକ୍ସରେ ଥିବା ଲିଙ୍କ୍ କୁ କ୍ଲିକ୍ କରନ୍ତୁ !!"
            #return redirect('homePage')
            return render(request ,'login.html' ,{'success': success_message} )

        else:

 # return render(request ,'signup.html' ,{'error' : error_message})# this error will be show in signupPage html using{%if error%}.alert.{%endif%}
           data={
               'error' : error_message ,
               'values' : value 
               

               }
            
           return render(request ,'signup.html' ,data)


def veryfy_from_profile(request):
    
    email = request.session.get('email')
    pf=CustomerLogUp.objects.filter(email=email).first()
    uid=pf.token
    success_message=None

    print(email)

    send_email_after_registration(email,uid)
     
    success_message ="To verify your account we sent a mail please click the link !!!"
     
    return render(request ,'login.html' ,{'success': success_message} )

def account_verify(request ,token):
            #print(token)
            pf=CustomerLogUp.objects.filter(token=token).first()
            #print(pf)
            pf.verify=True
            pf.save()
            success_message="ସଫଳତାର ସହ ଯାଞ୍ଚ କରାଯାଇଛି ଦୟାକରି ଲଗ୍ ଇନ୍ କରନ୍ତୁ।"
            return render(request ,'login.html' ,{'success': success_message} )

 

def loginPage(request):

    if request.method =='GET':
        return render(request , 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(email , password)
        customer = CustomerLogUp.get_customer_by_email(email)
        #print(customer)
        error_message= None
  
      
        #print(email ,password)
        if customer:
         fla = check_password(password ,customer.password)
         if fla:
             request.session['customer_id'] = customer.id
             request.session['email'] = customer.email
              
             return redirect('homePage')
         else:
             error_message='invalid email or password !!!'
       
        else:
            error_message='invalid email or password !!!'
         
         
        
        return render(request , "login.html" ,{'error': error_message})


def Logout(request):
        request.session.clear()
        return redirect("/log-in/")


def Cart(request):
    if request.method =='GET':
     #showing session  cart item  in html cart icon
     ids =list(request.session.get('cart').keys())
     #print(ids)
     s_products =Product.get_products_by_id(ids)
     #print(s_products)

     return render(request,"cart.html" ,{'s_products' :s_products})

    



    if request.method =='POST':
         
         
        id =request.POST.get('id')
        stock=request.POST.get('stock')

        #input_qty=request.POST.get('qty')

        
      
    cart = request.session.get('cart')
     
    if cart:
         quantity = cart.get(id)
         if quantity:
             
             if 'minus' in request.POST:
                 if quantity<=1:
                     cart.pop(id)
             
                 else:
  
                   cart[id] =quantity-1

             
             #if 'qty' in request.POST:
                 #cart[id] =input_qty



             
             if 'pluse' in request.POST:
                    if quantity >=int(stock):
                     error_massage="quantity not available"
                    else:
                      cart[id] =quantity+1



             if 'remove' in request.POST:
                 cart.pop(id)
         else:
             cart[id] = 1

    else:
         cart ={}
         cart[id] = 1

    request.session['cart'] = cart

    
     
    return redirect("/cart-in/")
 
    

     


def CheckOut(request):
   
      
    if request.method =='POST':

        #print(request.POST)
        ids =list(request.session.get('cart').keys())
        card_count=len(ids)
        #print(card_count)
        address = request.POST.get('Address')
        phone =  request.POST.get('Phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        #print(customer)
         


        for product in products:
            product_id=product.id
            product_name=product.name
            product_price=product.price
            order_quantity=cart.get(str(product.id))
            
            stock=product.stock
            if stock<=0:
                quantity_product_price=0

            else:
               quantity_product_price=int(order_quantity)*int(product_price)
             
            curent_stock=stock - order_quantity
            Product.objects.filter(id=product_id).update(stock=curent_stock)

             
            order = Order(customer = CustomerLogUp(id = customer ) ,
                          product = product ,
                          price = product.price ,
                            
                          address = address ,
                          phone = phone ,
                          quantity = cart.get(str(product.id)),
                          qnty_price= quantity_product_price,
                          stock =product.stock
                          
                              )
            
            order.save()
            
 
    #after save order data in order table send email 
    ids =list(request.session.get('cart').keys())
    customer = request.session.get('customer_id')
    s_products =Order.get_products_email_record(customer,card_count)
    #print(s_products)
    Total_price=Order.get_total_price(customer,card_count)
    #print(Total_price)
    Total_price_with_delevery=Total_price.get('qnty_price__sum')+20
    #print(Total_price_with_delevery)
    to=request.session.get('email')
         
             
    html_content=render_to_string("email_template.html",{'s_products' :s_products ,'Total_price':Total_price ,'Total_price_with_delevery':Total_price_with_delevery} )
        
    text_content =strip_tags(html_content)
    email= EmailMultiAlternatives(
        #subject
        'your order is sucssesful placed',

        #content
        text_content,

        #from email
        'kookoole45@gmail.com',
        #to email
        [to]
        )
    email.attach_alternative(html_content ,"text/html")
            
    email.send()
    #end email send  
           

    #after order saved we make cart empty
    request.session['cart'] = {}
        
    return redirect("/thanks/")
      

def OrdersStatus(request):
    if request.method =='GET':
        customer = request.session.get('customer_id')
        orders = Order.get_orders_by_customer(customer)
        #print(orders)
         
        return render(request ,'ordersstatus.html' ,{'orders': orders})


def Cancelation(request):
    if request.method =='GET':
        customer = request.session.get('customer_id')
        orders = Order.get_orders_by_customer(customer)
         
         
        return render(request ,'manageorders.html' ,{'orders': orders})
    if request.method =='POST':
        cancel = False
        ids =  request.POST.get('id')
        order_quantity = request.POST.get('q')
        product_id=request.POST.get('product_id')
        available_stock =request.POST.get('stock')
        current_stock= int(available_stock)+ int(order_quantity)
        
        print(ids)
        Order.objects.filter(id=ids).update(cancelation=cancel)
     
        Product.objects.filter(id=product_id).update(stock=current_stock)
        
         
        return redirect("/manage-orders/")


def Search(request):
    post=request.method =='POST'
    get=request.method =='GET'
    query= request.GET['query']
    qty=request.POST.get('qty')
    #allproducts= Product.objects.all()
    allproducts= Product.objects.filter(name__icontains=query)
    data ={'products': allproducts 
            
           }

    if  post:
     error_massage= None
     id =request.POST.get('id')
     stock=request.POST.get('stock')
     
     #print(id)
     cart = request.session.get('cart')
     
     if cart:
         quantity = cart.get(id)
         if quantity:
             if 'minus' in request.POST:
                 if quantity<=1:
                     cart.pop(id)
                 else:
  
                   cart[id] =quantity-1

             

             elif 'plus' in request.POST:
                 if quantity >=int(stock):
                     error_massage="quantity not available"
                 else:
                   cart[id] = quantity+1
             elif 'qty' in request.POST:
                  
                   if int(qty) <=int(stock):
                      cart[id] =int(qty)
                   else:
                       error_massage="quantity not available"
         else:
             cart[id] = 1

     else:
         cart ={}
         cart[id] = 1

     request.session['cart'] = cart
     
 

    return render(request,'search.html', data)


def Thanks(request):

    return render(request,'thankyou.html')


def Email(request):
       
     return render(request,"email_template.html")

def Emedit_profile_image(request):
    post=request.method =='POST'
    get=request.method =='GET'
  
    if  get:
        customer_first_name=None
        customer_last_name=None
        customer_phone=None
        customer_img=None
        #for user profile
        customer = request.session.get('email')
        customer_dtls=CustomerLogUp.objects.filter(email=customer)
        for i in customer_dtls:
            customer_first_name=i.first_name
            customer_last_name=i.last_name
            customer_phone=i.phone
            customer_img=i.profile_img
        #print(customer_first_name)
        #print(customer_last_name)
        #print(customer_phone)
        #print(customer_img)

        data ={}
     
         
        #for profile data
        data['customer_first_name'] = customer_first_name
        data['customer_last_name'] = customer_last_name
        data['customer'] = customer
        data['customer_phone'] = customer_phone
        data['customer_img'] = customer_img
        #end profile data
       
        return render(request,"edit_profile.html",data)
    if post and request.FILES['Customerimg']:
        customer_first_name=None
        customer_last_name=None
        customer_phone=None
        customer_img=None
        customer_first_name=request.POST.get('Firstname')
        customer_last_name=request.POST.get('Lastname')
        customer=request.POST.get('Email')
        customer_phone=request.POST.get('Phone')
        customer_img=request.FILES['Customerimg']
        fs=FileSystemStorage()
        filename=fs.save(customer_img.name,customer_img)
        url=fs.url(filename)
        #print(url)
         
        customer_dtls=CustomerLogUp.objects.filter(email=customer).first()
        customer_dtls.first_name=customer_first_name
        customer_dtls.last_name=customer_last_name
        customer_dtls.phone=customer_phone
        customer_dtls.profile_img=url
        #customer_dtls.permanate_address=
        customer_dtls.save()
     
        print(customer_first_name)
        print(customer_last_name)
        print(customer)
        print(customer_phone)
        print(customer_img)

        customer = request.session.get('email')
        customer_dtls=CustomerLogUp.objects.filter(email=customer)
        for i in customer_dtls:
            customer_first_name=i.first_name
            customer_last_name=i.last_name
            customer_phone=i.phone
            customer_img=i.profile_img
        #print(customer_first_name)
        #print(customer_last_name)
        #print(customer_phone)
        #print(customer_img)

        data ={}
     
         
        #for profile data
        data['customer_first_name'] = customer_first_name
        data['customer_last_name'] = customer_last_name
        data['customer'] = customer
        data['customer_phone'] = customer_phone
        data['customer_img'] = url
        #end profile data


        return render(request,"edit_profile.html",data)

def Emedit_profile_data(request):
    post=request.method =='POST'
    get=request.method =='GET'
  
    if  get:
        customer_first_name=None
        customer_last_name=None
        customer_phone=None
        customer_img=None
        #for user profile
        customer = request.session.get('email')
        customer_dtls=CustomerLogUp.objects.filter(email=customer)
        for i in customer_dtls:
            customer_first_name=i.first_name
            customer_last_name=i.last_name
            customer_phone=i.phone
            customer_img=i.profile_img
        #print(customer_first_name)
        #print(customer_last_name)
        #print(customer_phone)
        print(customer_img)

        data ={}
     
         
        #for profile data
        data['customer_first_name'] = customer_first_name
        data['customer_last_name'] = customer_last_name
        data['customer'] = customer
        data['customer_phone'] = customer_phone
        data['customer_img'] = customer_img
        #end profile data
       
        return render(request,"edit_profile.html",data)
    if post:
        customer_first_name=None
        customer_last_name=None
        customer_phone=None
        customer_img=None
        customer_first_name=request.POST.get('Firstname')
        customer_last_name=request.POST.get('Lastname')
        customer=request.POST.get('Email')
        customer_phone=request.POST.get('Phone')
        customer_img=request.POST.get('imageurl')
         
         
        customer_dtls=CustomerLogUp.objects.filter(email=customer).first()
        customer_dtls.first_name=customer_first_name
        customer_dtls.last_name=customer_last_name
        customer_dtls.phone=customer_phone
        customer_dtls.profile_img=customer_img
        
        customer_dtls.save()
     
        #print(customer_first_name)
        #print(customer_last_name)
        #print(customer)
        #print(customer_phone)
        #print(customer_img)

        customer = request.session.get('email')
        customer_dtls=CustomerLogUp.objects.filter(email=customer)
        for i in customer_dtls:
            customer_first_name=i.first_name
            customer_last_name=i.last_name
            customer_phone=i.phone
            customer_img=i.profile_img
        #print(customer_first_name)
        #print(customer_last_name)
        #print(customer_phone)
        #print(customer_img)

        data ={}
     
         
        #for profile data
        data['customer_first_name'] = customer_first_name
        data['customer_last_name'] = customer_last_name
        data['customer'] = customer
        data['customer_phone'] = customer_phone
        data['customer_img'] = customer_img
        #end profile data


        return render(request,"edit_profile.html",data)
     



def Forget_password_email(email,token):
    subject ="For get password"
    message = f'Hi click on the link to reset your account password http://127.0.0.1:8000/account_reset_password/{token}'
    from_email =settings.EMAIL_HOST_USER
    recipient_list =[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)

def Forget_password(request):
 post=request.method =='POST'
 success_message=None
 
 if post:
        postData = request.POST
         
        email =  postData.get('Email')
        #print(email)
        uid=uuid.uuid4()
        #print(uid)
        error_message=None
        
        if not CustomerLogUp.objects.filter(email=email).first():
            error_message ="No user found with this user email. !!!"
            #messages.success(request,'No user found with this user email.')
            return render(request , "forget_password.html" ,{'error': error_message})
        if CustomerLogUp.objects.filter(email=email).first():
           pc=CustomerLogUp.objects.filter(email=email).first()
           #print(pc)
           pc.password_reset_token=uid
           pc.save()
           Forget_password_email(email,uid)
           success_message ="କୁକୁଲ୍ ଆପଣଙ୍କ ମେଲ୍ କୁ ଏକ ଲିଙ୍କ୍ ପ୍ରେରଣ କରିଛି ।ଲିଙ୍କ୍ ଉପରେ କ୍ଲିକ୍ କରନ୍ତୁ ଏବଂ ଆପଣଙ୍କ ନୂତନ ପାସ୍ୱାର୍ଡ ପୁନଃସେଟ୍ କରନ୍ତୁ"
       
 return render(request,"forget_password.html",{'success': success_message})

def account_reset_password(request ,token):
    token=token
    if token:
       return render(request , "reset_password.html",{'token': token})
    return render(request,"forget_password.html")
       
 
def reset_password(request):
    post=request.method =='POST'
    if post:
        postData = request.POST
        error_message=None 
        success_message=None 
        new_password =postData.get('NewPassword')
        #print(new_password)
        conform_new_password =postData.get('ConformPassword')
        #print(conform_new_password)
        reset_password_token=postData.get('resetpasswordtoken')
        #print(reset_password_token)
        if new_password!=conform_new_password:
            error_message ="your password does not match. !!!"
            
            return render(request , "reset_password.html" ,{'error': error_message})

        if new_password==conform_new_password:
            pc=CustomerLogUp.objects.filter(password_reset_token=reset_password_token).first()
            print(pc)
            pc.password=make_password(new_password)
            pc.save()
            success_message ="ଆପଣଙ୍କ ପାସୱାର୍ଡ ସଫଳତାର ସହ ପରିବର୍ତ୍ତନ ହୋଇଛି। ଦୟାକରି ଲଗଇନ୍ କରନ୍ତୁ !!!"
            
            return render(request , "login.html" ,{'success': success_message})
    return render(request,"reset_password.html")     

def Change_your_password(request):
    
    post=request.method =='POST'
    get=request.method =='GET'
    success_message=None
    error_message=None
    email = request.session.get('email')
    pc = CustomerLogUp.objects.filter(email=email).first()
    curent_password=pc.password
    if get:
        return render(request , "change_your_password.html")

    if post:
        oldpassword=request.POST.get('oldpassword')
        
        new_password =request.POST.get('NewPassword')
        #print(new_password)
        conform_new_password =request.POST.get('ConformPassword')
        if not oldpassword:
            error_message='your old password is required'
            return render(request , "change_your_password.html" ,{'error': error_message})

        if not new_password:
            error_message='your new password is required'
            return render(request , "change_your_password.html" ,{'error': error_message})

        if not conform_new_password:
            error_message='your conform new password is required'
            return render(request , "change_your_password.html" ,{'error': error_message})

        fla = check_password(oldpassword ,curent_password)
        if  fla == False :
            error_message='your old password is incorect'
            return render(request , "change_your_password.html" ,{'error': error_message})

        if new_password != conform_new_password :
            error_message='your newpassword does not match with conform password'
            return render(request , "change_your_password.html" ,{'error': error_message})
        if  fla and new_password == conform_new_password:
            pc.password=make_password(new_password)
            pc.save()
            success_message =" password changed successfully !!!"
            return render(request , "login.html" ,{'success': success_message})
         
        return render(request , "change_your_password.html" ,{'error': success_message})

def Contact(request):
       
     return render(request,"contact.html")
      
def about(request):
       
     return render(request,"about.html")
         


     

   
