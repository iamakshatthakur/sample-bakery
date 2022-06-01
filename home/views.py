from django.shortcuts import render
from django.contrib.sessions import *
from django.contrib.auth.models import User,auth 
from django.shortcuts import render,redirect
from django.views import View
from .models import *
import razorpay
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.


def index(request):
    product_objects=Product.objects.all()
    cv=[]
    v=[]
    for ik in product_objects:
        if ik.category not in cv:
            cv.append(ik.category)
            v.append(ik)
    return render(request,'index.html',{'product_objects': product_objects ,'categry': v })

def registerpage(request):
    if request.method == 'POST':
        first_name = request.POST['First_name']
        last_name = request.POST['Last_name']
        email = request.POST['Email']
        username = request.POST['username']
        password = request.POST['Password']
        password2 = request.POST['Confirm_password']
        mobile = request.POST['mobile']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already exists")
                return redirect('/register')
            else:
                user = User.objects.create_user(
                email=email, password=password, first_name=first_name,last_name=last_name,username=username)
                user.save()
                send_mail(
                    'testing mail',
                    'welcome to the website of bakery your id has been successfully created',
                    'sample.mail.ak@gmail.com',
                    ['akthakur7865@gmail.com'],
                    fail_silently=True,
                    )

                messages.success(request, 'User Created Successfully')
                auth.login(request,user)
                return redirect('/')
        else:
            messages.error(request, "Password didn't match")
            return redirect('/register')
    else:
        return render(request,'register.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        userpassword = request.POST['userpassword']
        print(username,userpassword)
        any= auth.authenticate(request,username=username,password=userpassword)
        if any is not None:
            auth.login(request, any)
            messages.success(request, 'Logged in successfully !.....')
            return redirect('/')
        else:
            messages.warning(request, 'Invalid Credentials check username and password')
            return redirect('/login')

    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def breadpage(request):
    product_objects=Product.objects.all()
    bread_objects=Product.objects.filter(category__icontains='bread')
    return render(request,'bread.html',{'product_objects': product_objects , 'bread_objects': bread_objects})

def cakepage(request):
    cake_objects=Product.objects.filter(category__icontains='cakes')
    return render(request,'cakes.html',{'cakes': cake_objects})

def pastriespage(request):
    pastrie_objects=Product.objects.filter(category__icontains='pastries')
    return render(request,'pastries.html',{'pastries': pastrie_objects})

def cookiespage(request):
    cookie_objects=Product.objects.filter(category__icontains='cookies')
    return render(request,'cookies.html',{'cookies': cookie_objects})

def aboutpage(request):
    about_object=About.objects.all().first()
    print(about_object)
    return render(request,'about.html',{'about': about_object})


class detailpage(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            product_object=Product.objects.get(id=id)
            return render(request,'detail.html',{'product_object':product_object})
        else:
            return render(request,'register.html')
    def post(self,request,id):
        if request.user.is_authenticated:
            product=request.POST.get('productid') 
            remove=request.POST.get('remove')
            cart=request.session.get('cart')
            if product:
                if cart:
                    quantity=cart.get(product)
                    if quantity:
                        if quantity>=20:
                            cart[product]=20
                        else:
                            cart[product]=quantity+1
                    else:
                        cart[product]=1
                else:
                    cart={}
                    cart[product]=1

            if remove:
                quantity=cart.get(remove)
                if quantity:
                    if quantity==1:
                        cart.pop(remove)
                    else:
                        cart[remove]=quantity-1
                else:
                    pass
            request.session['cart']=cart
            product_object=Product.objects.get(id=id)
            return render(request,'detail.html',{'product_object':product_object})
        else:
            return render(request,'register.html')


class searchpage(View):
    def get(self,request):
        return render(request,'search.html')
    def post(self,request):
        searchitem=request.POST.get('searchitms')
        if(searchitem=="" or searchitem==" "or searchitem=="  "):
            return render(request,'search.html')
        else:
            search_objects=Product.objects.filter(product_name__icontains=searchitem)
            if len(search_objects)>=1:
                return render(request,'search.html',{'searchitems': search_objects})
            else:
                search_objects=Product.objects.filter(category__icontains=searchitem)
                return render(request,'search.html',{'searchitems': search_objects})

def blogpage(request):
    blogs=Blog.objects.all()
    return render(request,'blog.html',{'blogs':blogs})
    
def contactuspage(request):
    return render(request,'contactus.html')

class cartpage(View):
    def get(self,request):
        product_objects=Product.objects.all() 
        cart=request.session.get('cart')
        if cart:
            ids=request.session.get('cart').keys()
            cartitems=Product.objects.filter(id__in=ids)
            return render(request,'cart.html',{'product_objects':product_objects,'cartitems':cartitems})
        return render(request,'cart.html',{'product_objects':product_objects})
    def post(self,request):
        product_objects=Product.objects.all() 
        cart=request.session.get('cart')
        ids=request.session.get('cart').keys()
        if len(request.session.get('cart'))>=1:
            cartitems=Product.objects.filter(id__in=ids)
            print(request.POST)
            productid=request.POST.get('productid')
            action=int(request.POST.get('action'))
            print(cartitems)
            quantity=cart[productid]
            if quantity!=0:
                cart[productid]= quantity + action
                if cart[productid]>=20:
                    cart[productid]=20
                if cart[productid]==0:
                    cart.pop(productid)
            cartitems=Product.objects.filter(id__in=ids)
            request.session['cart']=cart
            return render(request,'cart.html',{'product_objects':product_objects,'cartitems':cartitems})

        return render(request,'cart.html',{'product_objects':product_objects})


class checkoutpage(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        if request.method == 'POST':
            print(request.POST)
            print(request.POST['finalprice'])
            final_price=request.POST['finalprice']
            return render(request,'checkout.html',{'finalprice':final_price})
           
class paytotalpage(View):
    def get(self,request):
        product_objects=Product.objects.all() 
        return render(request,'index.html',{'product_objects':product_objects})
    def post(self,request):
        product_objects=Product.objects.all() 
        cart=request.session.get('cart')
        if cart:
            ids=request.session.get('cart').keys()
            cartitems=Product.objects.filter(id__in=ids)
            address = request.POST['address']
            name = request.POST['name']
            email = request.POST['Email']
            mobile = request.POST['mobile']
            total_price = float(request.POST['finalprice'])
            customer=self.request.user
            items={}
            for product in cartitems:
                    x=str(product.id)
                    price=product.price
                    items[product.product_name]=cart[x]


            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))

            DATA = {
                "amount": total_price *100,
                "currency": "INR",
                "receipt": "receipt#1",
                "notes": {
                        "key1": "value3",
                        "key2": "value2"
                        }
                    }
            payment_order=client.order.create(data=DATA)
            payment_order_id=payment_order['id']
            print("order id",payment_order_id)
            userdetails={'address':address,'name':name,'email':email,'mobile':mobile,'total_price':total_price}
            final={'price':total_price,'api_key':settings.RAZORPAY_API_KEY,'order_id':payment_order_id}




            return render(request,'paytotal.html',{'product_objects':product_objects,'cartitems':cartitems,'userdetail':userdetails,"final":final})
        return render(request,'index.html',{'product_objects':product_objects})


class resultpage(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        print(request.POST)
        payment_id=request.POST['payment_id']
        order_id=request.POST['order_id']
        signature=request.POST['signature']
        userdetail=request.POST['userdetail']
        import ast
        userinfo=ast.literal_eval(userdetail)

        if payment_id!='payment_id' and order_id!='order_id' and signature!='signature' :
            payment ="success"
            print('payment success')
            cart=request.session.get('cart')
            ids=request.session.get('cart').keys()
            cartitems=Product.objects.filter(id__in=ids)
            items={}
            for product in cartitems:
                    x=str(product.id)
                    price=product.price
                    items[product.product_name]=cart[x]


            address=userinfo['address']
            name=userinfo['name']
            email=userinfo['email']
            mobile=userinfo['mobile']
            total_price=userinfo['total_price']
            customer=self.request.user

            Order=orderitem(customer=customer,product=items,price=total_price,name=name,address=address,phone=mobile,email=email,orderstatus='paid',razorpay_payment_id=payment_id,razorpay_order_id=order_id,razorpay_signature=signature)

            Order.placeorder()
            request.session['cart']={}



            return render(request,'result.html',{'success':payment})
        elif payment_id=='payment_id' and order_id=='order_id' and signature=='signature':
            payment="failure"
            error=request.POST['error']
            return render(request,'result.html',{'failed':'failed'})
        else:
            pass
            return render(request,'result.html')








