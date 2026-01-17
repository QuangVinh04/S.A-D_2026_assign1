from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book
from accounts.models import Customer

def get_customer_from_session(request):
    """Lấy customer từ session hoặc None"""
    customer_id = request.session.get('customer_id')
    if customer_id:
        try:
            return Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None
    return None

def add_to_cart(request, book_id):
    customer = get_customer_from_session(request)
    if not customer:
        messages.error(request, 'Please login to add items to cart.')
        return redirect('accounts:login')
    
    cart, _ = Cart.objects.get_or_create(customer=customer)
    book = get_object_or_404(Book, id=book_id)
    
    # Kiểm tra số lượng tồn kho
    if book.stock <= 0:
        messages.error(request, f'Sorry, "{book.title}" is out of stock.')
        return redirect('books:book_list')
    
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': 1}
    )
    if not created:
        if item.quantity >= book.stock:
            messages.warning(request, f'Cannot add more. Only {book.stock} items available.')
        else:
            item.quantity += 1
            item.save()
            messages.success(request, f'Added "{book.title}" to cart.')
    else:
        item.quantity = 1
        item.save()
        messages.success(request, f'Added "{book.title}" to cart.')
    
    return redirect('books:book_list')
    
def remove_item(request, item_id):
    customer = get_customer_from_session(request)
    if not customer:
        messages.error(request, 'Please login to remove items from cart.')
        return redirect('accounts:login')
    
    try:
        item = CartItem.objects.get(id=item_id, cart__customer=customer)
        item.delete()
        messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found.')
    
    return redirect('cart:cart_detail')

def view_cart(request):
    customer = get_customer_from_session(request)
    if not customer:
        messages.error(request, 'Please login to view your cart.')
        return redirect('accounts:login')
    
    cart, _ = Cart.objects.get_or_create(customer=customer)
    items = CartItem.objects.filter(cart=cart).select_related('book')
    
    total = sum(item.book.price * item.quantity for item in items)
    
    context = {
        'items': items,
        'total': total,
        'cart': cart,
    }
    return render(request, 'cart.html', context)