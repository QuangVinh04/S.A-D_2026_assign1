"""Django views - Framework layer"""
from django.shortcuts import render, redirect
from django.contrib import messages

# Use cases
from usecases.accounts.register_customer import RegisterCustomerUseCase
from usecases.accounts.login_customer import LoginCustomerUseCase
from usecases.books.get_book_catalog import GetBookCatalogUseCase
from usecases.cart.add_to_cart import AddToCartUseCase
from usecases.cart.view_cart import ViewCartUseCase
from usecases.cart.remove_from_cart import RemoveFromCartUseCase

# Repository implementations
from infrastructure.repositories.customer_repository_impl import DjangoCustomerRepository
from infrastructure.repositories.book_repository_impl import DjangoBookRepository
from infrastructure.repositories.cart_repository_impl import DjangoCartRepository

# Initialize repositories
customer_repo = DjangoCustomerRepository()
book_repo = DjangoBookRepository()
cart_repo = DjangoCartRepository()

# Initialize use cases
register_use_case = RegisterCustomerUseCase(customer_repo)
login_use_case = LoginCustomerUseCase(customer_repo)
get_books_use_case = GetBookCatalogUseCase(book_repo)
add_to_cart_use_case = AddToCartUseCase(cart_repo, book_repo)
view_cart_use_case = ViewCartUseCase(cart_repo)
remove_from_cart_use_case = RemoveFromCartUseCase(cart_repo)


def get_customer_id_from_session(request):
    """Helper to get customer ID from session"""
    return request.session.get('customer_id')


# Account views
def register_view(request):
    """Register view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')
        
        customer, error = register_use_case.execute(name, email, password)
        if error:
            messages.error(request, error)
            return render(request, 'accounts/register.html')
        
        messages.success(request, f'Account created for {customer.name}! You can now login.')
        return redirect('login')
    
    return render(request, 'accounts/register.html')


def login_view(request):
    """Login view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        customer, error = login_use_case.execute(email, password)
        if error:
            messages.error(request, error)
            return render(request, 'accounts/login.html')
        
        # Set session
        request.session['customer_id'] = customer.id
        request.session['customer_name'] = customer.name
        messages.success(request, f'Welcome back, {customer.name}!')
        return redirect('book_list')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logout view"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# Book views
def book_list_view(request):
    """Book catalog view"""
    books = get_books_use_case.execute()
    return render(request, 'books/list.html', {'books': books})


# Cart views
def add_to_cart_view(request, book_id):
    """Add to cart view"""
    customer_id = get_customer_id_from_session(request)
    if not customer_id:
        messages.error(request, 'Please login to add items to cart.')
        return redirect('login')
    
    cart_item, error = add_to_cart_use_case.execute(customer_id, book_id)
    if error:
        messages.error(request, error)
    else:
        messages.success(request, f'Added to cart!')
    
    return redirect('book_list')


def view_cart_view(request):
    """View cart"""
    customer_id = get_customer_id_from_session(request)
    if not customer_id:
        messages.error(request, 'Please login to view your cart.')
        return redirect('login')
    
    cart = view_cart_use_case.execute(customer_id)

    
    return render(request, 'cart/cart.html', {'cart': cart, 'items': cart.items, 'total': cart.total})


def remove_from_cart_view(request, item_id):
    """Remove from cart view"""
    customer_id = get_customer_id_from_session(request)
    if not customer_id:
        messages.error(request, 'Please login.')
        return redirect('login')
    
    error = remove_from_cart_use_case.execute(item_id)
    if error:
        messages.error(request, error)
    else:
        messages.success(request, 'Item removed from cart.')
    
    return redirect('view_cart')
