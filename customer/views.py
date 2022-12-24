 
from itertools import product
from urllib import request
from django.shortcuts import render,redirect
from . decorators import auth_customer
from customer.models import AddCart, Customer
from reseller_app.models import Product, Reseller
from django.db.models import F,Sum
from django.http import JsonResponse

# Create your views here.

def customer_home(request):
    msg = ""
    if request.method == 'POST':
        if 'c_signup' in request.POST:
            first_name = request.POST['fname']
            second_name = request.POST['sname']
            e_mail = request.POST['c_email']
            c_phone = request.POST['c_phno']
            c_password = request.POST['c_passwd']
            c_address = request.POST['c_addrs']
            email_exists = Customer.objects.filter(email = e_mail).exists()
            if not email_exists:
                customer = Customer(
                    first_name = first_name,
                    last_name =second_name,
                    email = e_mail,
                    mobile = c_phone,
                    password = c_password,
                    address = c_address)
                customer.save()
            else:
                msg="email already exists"      
            

        if 'c_login' in request.POST:
            email = request.POST['c_user_id']
            passwd = request.POST['c_user_passwd']

            try:
                customer = Customer.objects.get(email = email,password = passwd)
                request.session['c_id'] = customer.id
                
                 
            except:
                error_msg = 'Invalid Username Or Password'
                return render(request,'customer/customer_home.html',{'error_msg':error_msg})#customer end
     
   
        if 's_signup' in request.POST:
            s_name = request.POST['s_name']
            s_email = request.POST['s_email']
            s_mobile = request.POST['s_mobile']
            s_address = request.POST['s_address']
            s_account = request.POST['s_account']
            s_ifsc = request.POST['s_ifsc']
            s_acholder = request.POST['s_acholder']
            s_password = request.POST['s_password']
            s_pic = request.POST['s_pic']
            email_exists = Reseller.objects.filter(email = s_email).exists()
            # if not email_exists:

            reseller = Reseller(s_name = s_name,email = s_email,mobile = s_mobile,address = s_address,account_no =s_account,ifsc = s_ifsc,
            s_acholdername = s_acholder,password = s_password,s_pic = s_pic)
            reseller.save()
            # else:
            #     msg="email already exists"              

        if 'signin' in request.POST:

            email = request.POST['s_mail']
            passwd = request.POST['s_pass']
            print('seller')

            try:
                reseller = Reseller.objects.get(email = email,password = passwd)
                if reseller.s_status == "approved":
                    request.session['s_id'] = reseller.id               
                    return redirect("reseller:reseller_home")
                else:
                    error_msg = "your account not verified"
            except:
                error_msg = 'Invalid Username Or Password'
                return render(request,'customer/customer_home.html',{'error_msg':error_msg}) 
                   
    latest_product_list = Product.objects.all()
    cart_product_count = AddCart.objects.all().count()
    return render(request,'customer/customer_home.html',{'products':latest_product_list,'error_msg':msg,'cart_count':cart_product_count})
    

@auth_customer
def my_cart(request):
    
    return redirect('customer:view_cart') 

@auth_customer
def view_cart(request):    
    cart2=AddCart.objects.annotate(total_price = F('product__p_price') * F('qty'))
    sum=0
    for i in cart2:
        sum=sum+i.total_price

    #gt=AddCart.objects.aaggregate(grt =Sum( F('product__p_price') * F('qty')))
    gt=cart2.aaggregate(grt=Sum(F('total_price'))) 

    cart_product_count = AddCart.objects.all().count()
    return render(request,'customer/my_cart.html',{'cart_items':cart2,'gt':sum,'cart_count':cart_product_count})
    
@auth_customer
def del_cart_item(reqest,product_id):
    del_item=AddCart.objects.filter(product_id=product_id,customer_id=reqest.session['c_id'])
    del_item.delete()
    return redirect('customer:view_cart') 

@auth_customer
def my_order(request):
    cart_product_count = AddCart.objects.all().count()
    return render(request,'customer/my_orders.html',{'cart_count':cart_product_count})
@auth_customer
def product_detail(request,product_id):
    if request.method == "POST":
        p_id=request.POST['pid']
        p_qty=request.POST['qty'] 
        
        cart = AddCart(
        product_id = p_id ,
        qty=p_qty,
        customer_id = request.session['c_id'])

        if 'c_id' not in request.session: 
            msg="plase login"    
            return render(request,'customer/product_detail.html',{'product':product_detail,'error':msg})
        else:  
            product_exist=AddCart.objects.filter(product_id=p_id).exists()
            if not product_exist:
                cart.save()
            
        return redirect('customer:view_cart')


    product_detail=Product.objects.get(id=product_id)
    return render(request,'customer/product_detail.html',{'product':product_detail})

@auth_customer
def my_ac(request):
    customer_P=Customer.objects.get(id=request.session['c_id']) #select * from table where 

    cart_product_count = AddCart.objects.all().count()
    return render(request,'customer/my_account.html',{'customer_details':customer_P,'cart_count':cart_product_count})

@auth_customer
def edit_account(request):
    
    if request.method == 'POST':
        customer_edit=Customer.objects.get(id=request.session['c_id'])
        customer_edit.first_name = request.POST['edit_fname']
        customer_edit.last_name = request.POST['edit_lname']
        customer_edit.email = request.POST['edit_email']
        customer_edit.mobile = request.POST['edit_mobile']
        customer_edit.address = request.POST['edit_address']   
        customer_edit.save()
        return redirect('customer:my-account')

    customer_edit1=Customer.objects.get(id=request.session['c_id'])
    # view for save changes
    return render(request,'customer/editaccount.html',{'edit_details':customer_edit1})
    # customer_P=Customer.objects.get(id=request.session['c_id']) #select * from table where     
    # return render(request,'customer/my_account.html',{'customer_details':customer_P})
    
@auth_customer
def edit_form(request):
    return render(request,'customer/editform.html')

@auth_customer
def select_address(request):
     #select * from table where
    if request.method == 'POST':
        select_address=Customer.objects.get(id=request.session['c_id'])
        select_address.address = request.POST['address1']
        select_address.save()
        return redirect('customer:c_payment')
    
    customer_address1=Customer.objects.get(id=request.session['c_id'])
    return render(request,'customer/address.html',{'customer_address':customer_address1})

@auth_customer
def edit_addresss(request):
    
    if request.method == 'POST':
        new_address=Customer.objects.get(id=request.session['c_id'])
        new_address.name = request.POST['new_name']
        new_address.email = request.POST['new_email']
        new_address.mobile = request.POST['new_mobile']
        new_address.address = request.POST['new_address']   
        new_address.save()
        return redirect('customer:c_payment')
    #use this address
    # return render(request,'customer/editaddress.html',{'edit_details':customer_edit})
    return render(request,'customer/editaddress.html')

@auth_customer
def order_product(request):
    userid = request.session['c_id']
     


@auth_customer
def c_payment(request):
    return render(request,'customer/payment.html')

def c_logout(request):
    del request.session['c_id']
    request.session.flush()
    return redirect('customer:home')

def email_exist(request):
    email = request.POST['email']

    e_exists = Customer.objects.filter(email = email).exists()
    
    return JsonResponse({'status':e_exists})


def change_qty(request):
    quatity = int(request.POST['quantity'])
    p_id = request.POST['p_id']
    
    stock = Product.objects.get(id=p_id)
    print(stock.p_stock)
    print(quatity)
    if stock.p_stock > quatity:
        changeqty = AddCart.objects.get(id=p_id)
        changeqty.qty=quatity
        changeqty.save()
        status=True
        cart2=AddCart.objects.annotate(total_price = F('product__p_price') * F('qty'))
        sum=0
        for i in cart2:
            sum=sum+i.total_price
        msg="qty update successfully"
    
        return JsonResponse({'data':sum ,'status':status})
    else:
        status=False
        return JsonResponse({'status':status})
   