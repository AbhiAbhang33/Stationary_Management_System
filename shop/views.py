from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, Order

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})
'''
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    cart.products.add(product)
    cart.update_total()
    request.session['cart_id'] = cart.id
    return redirect('view_cart')
'''
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Option, CartItem
from .forms import AddToCartForm

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = AddToCartForm(request.POST, product=product)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            options = form.cleaned_data['options']
            quantity = form.cleaned_data['quantity']

            cart_item = CartItem.objects.create(
                product_id=product_id,
                quantity=quantity
            )
            cart_item.options.set(options)
            cart_item.save()

            return redirect('cart_detail')
    else:
        form = AddToCartForm(product=product)

    return render(request, 'add_to_cart.html', {'form': form, 'product': product})


def view_cart(request):
    cart = Cart.objects.get(id=request.session.get('cart_id'))
    return render(request, 'cart.html', {'cart': cart})

def checkout(request):
    cart = Cart.objects.get(id=request.session.get('cart_id'))
    if request.method == 'POST':
        address = request.POST['address']
        mobile_number = request.POST['mobile_number']
        order = Order.objects.create(cart=cart, address=address, mobile_number=mobile_number)
        del request.session['cart_id']
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'checkout.html', {'cart': cart})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})
