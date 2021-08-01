import re
from app.forms import ProfileForm, ReportForm, ServiceRequestForm, ContactForm,ReportForm
from typing import ContextManager
from django.shortcuts import render, redirect
from .models import  Equipment, Human_Resource, Order, Profile, ServiceRequest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.http.response import JsonResponse

# Create your views here.

def homeview(request):
    ctx ={'title':'welcome'}
    return render(request,'index.html',context= ctx)

def welcomeview(request):
    return render(request,'welcome.html')

def ordering(request):
        return render(request,'ordering.html')

def view_hr(request):
    hr= Human_Resource.objects.all()
    context = {'hr':hr}
    return render(request,'hr/view.html',context)  

def detail_hr(request,pk):
    hr= Human_Resource.objects.get(pk=pk)
    context = {'hr':hr}
    return render(request,'hr/detail.html',context)

def purchase(request):
    equipments = Equipment.objects.all()
    ctx = {'equipments':equipments}
    return render(request,'purchase/purchase.html',ctx)

def rent(request):
    return render(request,'rent_services/rent.html')

def service_request(request,pk):
    hr=Human_Resource.objects.filter(pk=pk)[0]
    form = ServiceRequestForm()
    if request.method=='POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            fd = form.save(commit = False)
            fd.hr=hr
            fd.for_user = request.user
            fd.save()
            messages.success(request,"Service request has been sent") 
            return redirect('home')
        else:
            messages.error(request,"Service request has not been sent") 
    context = {'form':form}
    return render(request,'hr/request_form.html', context)


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {'publicKey':settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config,safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method =='GET':
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price = request.GET.get('price')
        price = str(price).replace('.','0')+"00"
        if isinstance(request.session.get('cart'),dict):
            for k,v in request.session['cart'].items():
                print(v)
                product = Equipment.objects.get(id=v['product_id'])
                print(product)
                order = Order(buyer=request.user,product=product)
                order.save()
        else:
            print('no cart found')
        try:
            checkout_session = stripe.checkout.Session.create(
                # new
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {   
                        'name':'Medica Payment',
                        'quantity':1,
                        'currency':'inr',
                        'amount': int(price),
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def create_rent_session(request):
    if request.method =='GET':
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price = request.GET.get('price')
        price = str(price).replace('.','0')+"00"
        if isinstance(request.session.get('cart'),dict):
            for k,v in request.session['cart'].items():
                print(v)
                product = Equipment.objects.get(id=v['product_id'])
                print(product)
                order = Order(buyer=request.user,product=product)
                order.save()
        else:
            print('no cart found')
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {   
                        'name':'Medica Renting',
                        'quantity':1,
                        'currency':'inr',
                        'amount': int(price),
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def notify_success(request):
    messages.success(request,f"Your payment is complete.")
    cart = Cart(request)
    cart.clear()
    return render(request,"cart/success.html")

def notify_cancelled(request):
    messages.error(request,f"Your payment is cancelled.")
    return render(request,"cart/cancelled.html")

def user_profile(request):
    return render(request, 'user_profile/user.html')

def equipment(request):
    return render(request,'equipment/equipment.html')

@login_required
def user_profileview(request):
    users = Profile.objects.filter(user__pk=request.user.pk)
    if len(users)==1:
        context= {'userprofile':users}
    else:
        context = {'userprofile': None}
    return render(request, 'user_profile.html',context)

@login_required
def edit_profileview(request, pk):
    try:
        udata = Profile.objects.filter(pk=pk)
        if len(udata)==1:
            form = ProfileForm(instance=udata[0])
        else:
            form = ProfileForm()
        if request.method=='POST':
            if len(udata)==1:
                form = ProfileForm(request.POST, request.FILES, instance=udata[0])
            else:
                form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                fd=form.save(commit=False)
                fd.user=request.user
                fd.email=request.user.email
                fd.save()
                messages.success(request,"User Profile has been updated") 
                return redirect('up')
        
        context = {"pform":form}
        return render(request, 'edit_profile.html', context)
    except Exception as e:
        print('some error occurred',e)
        return redirect('up')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        # when u fill the form, post method activities
        form = ContactForm(request.POST)
        # if all the data in form is okay
        
        if form.is_valid():
            # save it into database
            form.save()
            # redirect the page
            messages.success(request,"Contact has been save") 
            return redirect('contact') 
    else:
        # when u just open the page to view the form
        form = ContactForm() # Khali form

    # put info in the context to send it into page
    context = {'c_form':form}
    # set which page to load
    return render(request,'contactus.html',context)

@login_required
def report(request):
    if request.method== 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            messages.success(request,"Report has been sent") 
            return redirect('report')
        else:
            messages.error(request,"Report has not been sent") 
    else:
        form = ReportForm()
    context = {'c_form':form}
    return render(request,'report.html', context)

@login_required()
def cart_add(request, id):
    cart = Cart(request)
    product = Equipment.objects.get(id=id)
    cart.add(product=product)
    messages.success(request,f"Successfully added {product.name} to cart")
    return redirect("pc")


@login_required()
def item_clear(request, id):
    cart = Cart(request)
    product = Equipment.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required()
def item_increment(request, id):
    cart = Cart(request)
    product = Equipment.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required()
def item_decrement(request, id):
    cart = Cart(request)
    product = Equipment.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required()
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required()
def cart_detail(request):
    total = 0
    for k,v in request.session.get('cart').items():
        qty = v.get("quantity")
        price = v.get("price")
        total +=int(qty)*int(price)
    # print(total)
    ctx = {'total':total}
    return render(request, 'cart/cart_detail.html',ctx)





            
    

 
