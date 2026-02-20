from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, MenuItem, Order, OrderItem, Reservation, Review
from django.contrib import messages
from django.db import transaction
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import json

def home(request):
    categories = Category.objects.all().order_by('name')
    menu_items = MenuItem.objects.filter(is_available=True).order_by('category__name', 'name')
    reviews = Review.objects.all().select_related('menu_item', 'user').order_by('-created_at')[:5]
    
    # Get real statistics
    menu_items_count = MenuItem.objects.filter(is_available=True).count()
    
    # Calculate average rating from reviews
    avg_rating_data = Review.objects.aggregate(avg_rating=Avg('rating'))
    average_rating = avg_rating_data['avg_rating'] or 0
    
    # Calculate years of service (based on when the first review was created)
    first_review = Review.objects.order_by('created_at').first()
    if first_review:
        years_serving = (datetime.now().date() - first_review.created_at.date()).days // 365
        if years_serving < 1:
            years_serving = 1
    else:
        years_serving = 10  # Default fallback
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'reviews': reviews,
        'menu_items_count': menu_items_count,
        'average_rating': round(average_rating, 1) if average_rating else 0,
        'years_serving': years_serving,
    }
    return render(request, 'restaurant/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-order_date')
    user_reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    user_reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'user_orders': user_orders,
        'user_reservations': user_reservations,
        'user_reviews': user_reviews,
    }
    return render(request, 'restaurant/profile.html', context)

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart[item_id_str]['quantity'] += 1
    else:
        cart[item_id_str] = {
            'name': item.name,
            'price': float(item.price),
            'quantity': 1,
            'image': item.image.url if item.image else None,
        }
    
    request.session['cart'] = cart
    messages.success(request, f'{item.name} added to cart!')
    return redirect('home')

@login_required
def cart_view(request):
    cart_items = []
    total_price = 0
    
    if 'cart' in request.session:
        for item_id, item_data in request.session['cart'].items():
            item_total = item_data['price'] * item_data['quantity']
            cart_items.append({
                'item_id': item_id,
                'name': item_data['name'],
                'price': item_data['price'],
                'quantity': item_data['quantity'],
                'subtotal': item_total,
                'image': item_data.get('image'),
            })
            total_price += item_total
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'restaurant/cart.html', context)

@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        
        if 'cart' in request.session:
            cart = request.session['cart']
            item_id_str = str(item_id)
            
            if item_id_str in cart:
                if quantity <= 0:
                    del cart[item_id_str]
                else:
                    cart[item_id_str]['quantity'] = quantity
                
                request.session['cart'] = cart
        
        messages.success(request, 'Cart updated successfully!')
    
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        if 'cart' in request.session:
            cart = request.session['cart']
            item_id_str = str(item_id)
            
            if item_id_str in cart:
                del cart[item_id_str]
                request.session['cart'] = cart
                messages.success(request, 'Item removed from cart!')
    
    return redirect('cart_view')

@login_required
def checkout(request):
    if 'cart' in request.session and request.session['cart']:
        cart_items = []
        total_amount = 0
        
        for item_id, item_data in request.session['cart'].items():
            item_total = item_data['price'] * item_data['quantity']
            cart_items.append({
                'menu_item_id': int(item_id),
                'quantity': item_data['quantity'],
                'subtotal': item_total,
            })
            total_amount += item_total
        
        if request.method == 'POST':
            customer_name = request.POST.get('customer_name')
            customer_email = request.POST.get('customer_email')
            customer_phone = request.POST.get('customer_phone', '')
            
            if customer_name and customer_email:
                # Create order
                with transaction.atomic():
                    order = Order.objects.create(
                        user=request.user,
                        customer_name=customer_name,
                        customer_email=customer_email,
                        customer_phone=customer_phone,
                        total_amount=total_amount,
                        status='Pending',
                    )
                    
                    # Add order items
                    for item in cart_items:
                        menu_item = get_object_or_404(MenuItem, id=item['menu_item_id'])
                        OrderItem.objects.create(
                            order=order,
                            menu_item=menu_item,
                            quantity=item['quantity'],
                            price=menu_item.price,
                        )
                
                # Clear cart
                request.session['cart'] = {}
                
                messages.success(request, f'Order #{order.id} placed successfully! Our team will process it shortly.')
                return redirect('home')
            else:
                messages.error(request, 'Please fill in all required fields.')
        
        # For GET request, prepare form with potential user data
        customer_name = request.user.first_name + ' ' + request.user.last_name if request.user.first_name or request.user.last_name else request.user.username
        customer_email = request.user.email
        
        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
            'customer_name': customer_name,
            'customer_email': customer_email,
        }
        return render(request, 'restaurant/checkout.html', context)
    else:
        messages.error(request, 'Your cart is empty.')
        return redirect('home')

def reservation_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_guests = request.POST.get('number_of_guests')
        special_requests = request.POST.get('special_requests', '')
        
        if name and email and date and time and number_of_guests:
            try:
                reservation = Reservation.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=name,
                    email=email,
                    phone=phone,
                    date=date,
                    time=time,
                    number_of_guests=int(number_of_guests),
                    special_requests=special_requests,
                    confirmed=False,
                )
                messages.success(request, 'Reservation request submitted successfully! We will confirm your reservation shortly.')
                return redirect('home')
            except ValueError:
                messages.error(request, 'Invalid number of guests.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'restaurant/reservation.html')

def contact_us(request):
    return render(request, 'restaurant/contact_us.html')

def submit_review(request):
    menu_items = MenuItem.objects.filter(is_available=True)
    
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        if menu_item_id and rating:
            try:
                menu_item = get_object_or_404(MenuItem, id=menu_item_id)
                Review.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    menu_item=menu_item,
                    rating=int(rating),
                    comment=comment,
                )
                messages.success(request, 'Thank you for your review!')
                return redirect('home')
            except ValueError:
                messages.error(request, 'Invalid rating value.')
        else:
            messages.error(request, 'Please select a menu item and rating.')
    
    context = {
        'menu_items': menu_items,
    }
    return render(request, 'restaurant/review_form.html', context)