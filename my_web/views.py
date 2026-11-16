from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .models import product, category
from django.db.models import Q
from django.shortcuts import render



# Create your views here.



def registration(request):
    if request.method == 'POST':
        data = request.POST
        if data:
            User.objects.create_user(username = data['username'],password = data['password'])
        else:
            return redirect("registration")
        return redirect("login")
    return render(request, 'registration.html')
    
        

def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(request, username = data['username'], password = data['password'])
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            return redirect("login")
    return render(request, 'login.html')





@login_required
def logout_user(request):
    logout(request)
    return redirect("login")



@login_required
def profile(request):
    return render(request, 'profile.html')






def create_order(request, pk):
    product = get_object_or_404(product, pk=pk)
    if request.method == "POST":
        data = request.POST
        order = order.objects.create(
            customer_name = data['customer_name'],
            count = data['count'],
        )
        product = product
        product.stock -= int(data['count'])
        product.save()
        order.product_id.add(product)
        return redirect('get_products')
    
    return render(request, 'add_orders.html', {"product": product})
    


    
def get_products(request):
    query = request.GET.get('q')
    products=product.objects.all()
    if query:
        products=products.filter(
            product_name__icontains = query
        )
    return render(request, 'show_products.html', {"products":products, 'query':query})



def categories(request):
    categories = category.objects.all()
    return render(request, 'categories.html', {'categories': categories})





def products(request):
    products = product.objects.all()
    categories = category.objects.all()

    return render(request, 'products.html', {'products': products,'categories': categories})





def orders(request):
    orders = order.objects.all()
    return render(request, 'orders.html', {'orders': orders})




def add_category(request):
    if request.method == 'POST':
        category.objects.create(
            category_name=request.POST.get('category_name')
        )
        return redirect('categories')
    return render(request, 'add_category.html')





def add_product(request):
    if request.method == 'POST':
        product.objects.create(
            product_name=request.POST.get('product_name'),
            category_id=category.objects.get(
                id=request.POST.get('category_id')
            ),
            price=request.POST.get('price'),
            photo=request.FILES.get('photo'),
            stock=request.POST.get('stock')
        )
        return redirect('products')
    return render(request, 'add_product.html', {'categories': category.objects.all()})





def home(request):
    return render(request, 'home.html')




def deals(request):
    products = product.objects.filter(is_active=True)
    return render(request, 'products.html', {'products': products})




def wishlist(request):
    return render(request, 'home.html') 





def show_products(request):
    search = request.GET.get('search', '').strip()

    products = product.objects.filter(is_active=True)

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    return render(request, 'shop/show_product.html', {
        'products': products,
        'search': search,
    })




def show_categories(request):
    search = request.GET.get('search', '').strip()

    categories = category.objects.filter(is_active=True)

    if search:
        categories = categories.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    return render(request, 'categories.html', {
        'categories': categories,
        'search': search,
    })
