from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import product as Product
from .models import category as Category
from .models import order as Order


def registration(request):
    if request.method == 'POST':
        data = request.POST
        User.objects.create_user(
            username=data['username'],
            password=data['password']
        )
        return redirect('login')
    return render(request, 'registration.html')




def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(
            request,
            username=data['username'],
            password=data['password']
        )
        if user is not None:
            login(request, user)
            return redirect('profile')
        return redirect('login')
    return render(request, 'login.html')





@login_required
def logout_user(request):
    logout(request)
    return redirect('login')






@login_required
def profile(request):
    return render(request, 'profile.html')




def home(request):
    return render(request, 'home.html')





def products(request):
    search = request.GET.get('search', '').strip()
    category_id = request.GET.get('category')
    product_list = Product.objects.filter(is_active=True)
    if search:
        product_list = product_list.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if category_id:
        product_list = product_list.filter(category_id=category_id)
    return render(request, 'show_products.html', {
        'products': product_list,
        'search': search
    })






def show_categories(request):    
    categories = Category.objects.filter(is_active=True)
    return render(request, 'categories.html', {
        'categories': categories
    })


def deals(request):
    product_list = Product.objects.filter(is_active=True)

    return render(request, 'show_products.html', {
        'products': product_list
    })






def wishlist(request):
    return render(request, 'home.html')






@login_required
def create_order(request, pk):
    selected_product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True
    )

    if request.method == 'POST':
        data = request.POST
        quantity = int(data.get('quantity', 1))

        Order.objects.create(
            user=request.user,
            product=selected_product,
            customer_name=data.get('customer_name'),
            phone_number=data.get('phone_number'),
            quantity=quantity,
            total_price=selected_product.price * quantity
        )

        return redirect('orders')

    return render(request, 'get_order.html', {
        'product': selected_product
    })




@login_required
def orders(request):
    user_orders = Order.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('product').order_by('-created_at')

    return render(request, 'orders.html', {
        'orders': user_orders
    })


@login_required
def update_order(request, pk):
    current_order = get_object_or_404(
        Order,
        pk=pk,
        user=request.user,
        is_active=True
    )

    if request.method == 'POST':
        data = request.POST

        current_order.customer_name = data.get('customer_name')
        current_order.phone_number = data.get('phone_number')
        current_order.quantity = int(data.get('quantity', 1))
        current_order.total_price = (
            current_order.product.price * current_order.quantity
        )

        current_order.save()

        return redirect('orders')

    return render(request, 'edit_order.html', {
        'order': current_order
    })


@login_required
@require_POST
def delete_order(request, pk):
    current_order = get_object_or_404(
        Order,
        pk=pk,
        user=request.user,
        is_active=True
    )

    current_order.is_active = False
    current_order.save()

    return redirect('orders')


@login_required
def add_category(request):
    if request.method == 'POST':
        Category.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('categories')

    return render(request, 'add_category.html')


@login_required
def add_product(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            category=Category.objects.get(
                id=request.POST.get('category_id')
            ),
            price=request.POST.get('price'),
            photo=request.FILES.get('photo')
        )

        return redirect('products')

    return render(request, 'add_product.html', {
        'categories': Category.objects.all()
    })
