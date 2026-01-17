from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerRegistrationForm, CustomerLoginForm
from cart.models import Cart

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Account created for {customer.name}! You can now login.')
            return redirect('accounts:login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                customer = Customer.objects.get(email=email)
                if customer.check_password(password):
                    # Lưu customer_id vào session
                    request.session['customer_id'] = customer.id
                    request.session['customer_name'] = customer.name
                    messages.success(request, f'Welcome back, {customer.name}!')
                    
                    # Tạo giỏ hàng nếu chưa có
                    Cart.objects.get_or_create(customer=customer)
                    
                    # Redirect về trang trước đó hoặc book list
                    next_url = request.GET.get('next', 'books:book_list')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid email or password.')
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomerLoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

def profile(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Please login to view your profile.')
        return redirect('accounts:login')
    
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'profile.html', {'customer': customer})