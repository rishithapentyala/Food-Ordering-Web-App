from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import *
from django.contrib import messages
from .form import CustomUserForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    # return HttpResponse('<h1>this is the home page</h1>')
    items = Items.objects.filter(underrated_item=True)
    new_items = Items.objects.filter(new_added_item=True)
    return render(request,'home.html',{'items':items,'new_items':new_items})

def login_page(request):
    if request.method == "POST":
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in successfully.')
        else:
            messages.error(request,'Invalid username or password.')
            return redirect('Login') 
    return render(request,'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged out successfully!')
    return redirect('Login') 

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('Login') 
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserForm()  # Create a new instance of the form

    return render(request, 'register.html', {'form': form})


def category(request):
    categories = Category.objects.all()
    return render(request,'categories.html',{'categories':categories})

def categoryview(request, name):
    # Try to get the category by name
    try:
        category = Category.objects.get(food_names=name)
        
        # Filter items by the category instance
        items = Items.objects.filter(category=category)

        # If there are no items, show a warning message
        if not items:
            messages.warning(request, 'No items found for this category.')

        return render(request, 'item_view.html', {'items': items, 'category': category})

    except Category.DoesNotExist:
        # If the category does not exist, show an error message and redirect
        messages.error(request,"Oops! It seems we couldn't find that category. Please try a different one!")
        return redirect('Category')  # Replace 'homepage' with the URL name you want to redirect to

def productdetail(request, cname, pname):
    try:
        # Check if the category exists
        category = Category.objects.get(food_names=cname)

        # Check if the item exists in the given category
        item = Items.objects.get(name=pname, category=category)

        # If the item is found, render the product details page
        return render(request, 'product_detail.html', {'item': item})

    except Category.DoesNotExist:
        # Handle case where the category does not exist
        messages.error(request, "Oops! It seems we couldn't find that category. Please try a different one!")
        return redirect('Category')  # Replace 'homepage' with your desired redirection

    except Items.DoesNotExist:
        # Handle case where the product does not exist in the specified category
        messages.error(request, 'Oops! It looks like there are no food items in this category. How about exploring other delicious options?')
        return redirect('Category', name=cname)  # Redirect to the category page or another page

def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['product_id']
            product_status = Items.objects.get(id=product_id)
            if product_status:
                # in Django's ORM syntax, you can't use dot notation in filter conditions like product.id. Instead, you should use the double underscore __ notation to access the id field of the ForeignKey.
                # "why using double underscore" - use this when you want to filter on other fields of the related model, e.g., product__name or product__price.
                if Cart.objects.filter(user=request.user,product_id=product_id).exists(): 
                    cart_qty_update = Cart.objects.get(user=request.user, product_id=product_id)
                    cart_qty_update.product_qty = product_qty
                    cart_qty_update.save()
                    return JsonResponse({'status':'Product quantity updated in Cart'}, status = 200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty )
                        return JsonResponse({'status':'Product added to Cart'}, status = 200)
                    else:
                        return JsonResponse({'status':'Product stock not available'}, status = 200)
        else:
            return JsonResponse({'status':'Please Login to add items to your cart'}, status = 200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status = 200)

def cart_page(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.product.offer_price * item.product_qty for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
        }
        return render(request,'cart.html',{'cart_items':cart_items,'total_amount':total_amount})
    else:
        messages.error(request, 'please login to enter cart page')
        return redirect('Login')

def remove_cart(request,Cartid):
    cart_item = Cart.objects.get(id = Cartid)
    cart_item.delete()
    return redirect('Cart')

def add_to_fav(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['product_id']
            product_status = Items.objects.get(id=product_id)
            if product_status:
                # in Django's ORM syntax, you can't use dot notation in filter conditions like product.id. Instead, you should use the double underscore __ notation to access the id field of the ForeignKey.
                # "why using double underscore" - use this when you want to filter on other fields of the related model, e.g., product__name or product__price.
                if Favourite.objects.filter(user=request.user,product_id=product_id).exists(): 
                    return JsonResponse({'status':'Product already in favourite list'}, status = 200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id )
                    return JsonResponse({'status':'Product added to favourite list'}, status = 200)
        else:
            return JsonResponse({'status':'Please Login to add items to your cart'}, status = 200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status = 200)

def favourite_page(request):
    if request.user.is_authenticated:
        fav_items = Favourite.objects.filter(user=request.user)
        return render(request,'favourite.html',{'fav_items':fav_items})
    else:
        messages.error(request, 'please login to enter Favourite page')
        return redirect('Login')

def remove_fav(request,favid):
    fav_item = Favourite.objects.get(id = favid)
    fav_item.delete()
    return redirect('Favourite')