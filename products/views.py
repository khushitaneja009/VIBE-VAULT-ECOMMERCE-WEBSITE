from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def category_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to browse categories')
        return redirect('login')
    categories = Category.objects.all()
    return render(request, 'products/category.html', {'categories': categories})

def product_list(request, category_id=None):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view products')
        return redirect('login')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'products/produts.html', {'products': products})

def product_detail(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view product details')
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()  # Get all items in the user's cart
        total_price = cart.get_cart_total()  # Method you added in Cart model
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create a CartItem for the selected product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If it already exists, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        cart_count = cart.cartitem_set.count()
        return JsonResponse({'success': True, 'count': cart_count})
    
    return redirect('cart_view')


@login_required
def cart_count(request):
    """Return the number of items in cart as JSON"""
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.cartitem_set.count()
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})

    cart_item.save()

    return redirect('cart_view')



@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "increase":
            item.quantity += 1

        elif action == "decrease" and item.quantity > 1:
            item.quantity -= 1

        item.save()

    return redirect('cart_view')


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')

@login_required
def Order_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        total_price = cart.get_cart_total()  # Method you added in Cart model
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    
    return render(request, 'products/order.html', {
        'total_price': total_price
    })



@login_required
def submit_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        # Clear cart after order
        cart = Cart.objects.get(user=request.user)
        cart.cartitem_set.all().delete()

        
        #return redirect('all_products')
    return redirect('Thanks_view')

def thank_you(request):
    messages.success(request, "Order placed successfully!")
    print(request.user.username)
    return render(request, 'products/Thanku.html', {'user_name': request.user.username})
   