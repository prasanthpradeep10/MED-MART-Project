from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Registration,Category,Order,Product,Rating1,OrderItem,CartItem,DeliveryBoyStatus
from .forms import CategoryForm,ProductForm,CheckoutForm,RatingForm,UsernameUpdateForm,EmailUpdateForm,CustomPasswordChangeForm,AddressForm,AddressEditForm,AssignDeliveryBoyForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout 
from .models import Address
import json
from geopy.geocoders import Nominatim
import time
from .utils import haversine
import requests 
from geopy.distance import geodesic 
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from django.utils import timezone






def index(request):
    return render(request,'extt/index.html')

def user_home(request):
    return render(request,'extt/user_home.html')

def admin_home(request):
    # Fetch an order (make sure it has an id)
    order = Order.objects.first()  # Or some logic to get a specific order
    return render(request, 'extt/admin_home.html', {'order': order})

def about(request):
    return render(request, 'extt/about.html')


def admin_reg(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password == confirmpassword:
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username already taken")
                return redirect('admin_reg')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already taken")
                return redirect('admin_reg')
            else:
                admin_reg = User.objects.create_user(username = username,email = email,password = password)
                admin_reg.save()
                gtg = Registration()
                gtg.user_role = 'admin'
                gtg.password = password
                gtg.user = admin_reg
                gtg.save()
                messages.info(request,"Successfully created")
                return redirect('login')
        else:
            messages.info(request,"Password doesn't match")
            return redirect('admin_reg')

    return render(request,'extt/admin_reg.html')

def user_reg(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password == confirmpassword:
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username already taken")
                return redirect('user_reg')
            elif User.objects.filter(email = email).exists():
                messages.info(request,"Email already taken")
                return redirect('user_reg')
            else:
                user_reg = User.objects.create_user(username = username,email = email,password = password)
                user_reg.save()
                gtg = Registration()
                gtg.user_role = 'customer'
                gtg.password = password
                gtg.user = user_reg
                gtg.save()
                
                messages.info(request,"Successfully created")
                return redirect('login')
        else:
            messages.info(request,"Password doesn't match")
            return redirect('user_reg')

    return render(request,'extt/user_reg.html')


def delivery_boy_reg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('delivery_boy_reg')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('delivery_boy_reg')
            else:
                delivery_boy_user = User.objects.create_user(username=username, email=email, password=password)
                delivery_boy_user.save()
                
                # Create the registration record for the delivery boy
                registration = Registration()
                registration.user_role = 'delivery_boy'  # Set the role to 'delivery_boy'
                registration.password = password
                registration.user = delivery_boy_user
                registration.save()
                
                messages.info(request, "Delivery boy registered successfully.")
                return redirect('login')
        else:
            messages.info(request, "Password doesn't match")
            return redirect('delivery_boy_reg')

    return render(request, 'extt/delivery_boy_reg.html')

    
def log(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            # Check the role of the user and redirect accordingly
            if user.is_superuser:
                return redirect('admin_home')

            # Check if the user has a registration profile and get the role
            if hasattr(user, 'registration'):
                user_role = user.registration.user_role

                if user_role == 'customer':
                    return redirect('user_home')  # Redirect to user home page
                elif user_role == 'delivery_boy':
                    return redirect('delivery_boy_home')  # Redirect to delivery boy home page
                elif user_role == 'admin':
                    return redirect('admin_home')  # Redirect to admin home page

                else:
                    messages.error(request, 'Invalid user role assigned.')
                    return redirect('login')  # Redirect back to login page

            else:
                # If no registration profile, handle it accordingly
                messages.error(request, 'No registration profile found for this user.')
                return redirect('login')

        else:
            # Display an error message for invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to login page
    else:
        # Render the login form
        return render(request, 'extt/login.html')
            
            
            

def logout(request):
    auth.logout(request)
    return redirect('index')



def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category')  
    else:
        form = CategoryForm()
    
    return render(request, 'extt/add_category.html', {'form': form})

def demo_category(request):
    categories = Category.objects.all()
    return render(request, 'extt/demo_category.html', {'cat': categories})

def category(request):
    categories = Category.objects.all()
    return render(request, 'extt/category.html', {'cat': categories})


def demo_products(request, cat_id):
    category = Category.objects.get(id = cat_id)
    ctt = int(category.id)
    request.session['catt_idd'] = category.id
    products = Product.objects.filter(category = ctt)
    star_range = range(1, 6) 
    return render(request, 'extt/demo_products.html', {'category': category, 'products': products,'star_range': star_range})


def products(request, cat_id):
    category = Category.objects.get(id = cat_id)
    ctt = int(category.id)
    request.session['catt_idd'] = category.id
    products = Product.objects.filter(category = ctt)
    star_range = range(1, 6) 
    
    return render(request, 'extt/products.html', {'category': category, 'products': products,'star_range': star_range})

def add_products(request, cat_id):
    category = Category.objects.get(id = cat_id)
   
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            return redirect('products', cat_id=category.id)
    else:
        form = ProductForm()

    return render(request, 'extt/add_product.html', {'form': form, 'category': category})

def product_edit(request, hy):
    product = Product.objects.get(id = hy)
    cat = Category.objects.get(id = request.session['catt_idd'])
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            redd = '/products/'+str(cat.id)
            return redirect(redd)  
    else:
        form = ProductForm(instance=product)
    return render(request, 'extt/product_edit.html', {'form': form, 'product': product})

def product_delete(request, hy):
    product = Product.objects.get(id = hy)
    cat = Category.objects.get(id = request.session['catt_idd'])
    if request.method == 'POST':
        product.delete()
        redd = '/products/'+str(cat.id)
        return redirect(redd)  
         
    return render(request, 'extt/product_delete.html', {'product': product})


def user_category(request):
    categories = Category.objects.all()
    return render(request, 'extt/user_category.html', {'cat': categories})



def user_products(request, cat_id):
    category = Category.objects.get(id = cat_id)
    ctt = int(category.id)
    request.session['catt_idd'] = category.id
    products = Product.objects.filter(category = ctt)
    star_range = range(1, 6) 
    return render(request, 'extt/user_products.html', {'category': category, 'products': products,'star_range': star_range})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    cart_item, created = CartItem.objects.get_or_create(user = request.user, product = product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user = request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'extt/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id = item_id, user = request.user)
    cart_item.delete()
    return redirect('cart')

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        messages.error(request, "Quantity cannot be less than 1.")
    
    cart_item.save()
    return redirect('cart') 

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)  # Pass user to form
        if form.is_valid():
            selected_address = form.cleaned_data['address']

            # Create the order
            order = Order.objects.create(
                user=request.user,
                address=selected_address,
                total_price=total_price,
            )

            # Create OrderItems for each CartItem
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    total_price=cart_item.total_price(),
                )

            # Clear the cart after creating the order
            cart_items.delete()

            # Prepare the HTML email content
            subject = 'Your Order Invoice - MEDMART'
            html_content = render_to_string('extt/order_invoice.html', {
                'user': request.user,
                'order': order,
                'cart_items': CartItem.objects.filter(user=request.user),  # Re-fetch cart items after clearing the cart
                'total_price': total_price,
            })
            recipient_email = request.user.email

            # Send the email with HTML content
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )
            email.content_subtype = 'html'  # Specify that the email content is HTML
            email.send(fail_silently=False)

            return redirect('order_success')
    else:
        form = CheckoutForm(user=request.user)

    return render(request, 'extt/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    })

@login_required
def order_success(request):
    return render(request, 'extt/order_success.html')

def orders_list(request):
    # Fetch orders in descending order by the `created_at` field
    orders = Order.objects.prefetch_related('order_items__product').order_by('-created_at')
    return render(request, 'extt/orders_list.html', {'orders': orders})



@login_required
def order_history(request):
    # Retrieve all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Show latest orders first
    return render(request, 'extt/order_history.html', { 'orders': orders, })
    
def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    
    return render(request, 'extt/search.html', {'products': products, 'query': query})


def user_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    
    return render(request, 'extt/user_search.html', {'products': products, 'query': query})


def suggestion(request):
    query = request.GET.get('query', '')

    if query:
        products = Product.objects.filter(name__icontains=query)[:5]  # Limit to 5 suggestions
    else:
        products = []

    html = render_to_string('extt/suggestion.html', {'products': products})
    
    return JsonResponse(html, safe=False)


def rate_product(request, order_id, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            print(product_id)
            # Create a new rating instance but don't save to DB yet
            rating = form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.order = order
            # Now save to the database with all fields set
            rating.save()
            return redirect('rate_success') 
    else:
        # Create an empty form instance for GET request
        form = RatingForm()

    return render(request, 'extt/rate_product.html', {'form': form, 'product': product, 'order': order})

def rate_success(request):
    return render(request, 'extt/rate_success.html')


@login_required
def user_profile(request, username):
    # Get the user by username
    user = get_object_or_404(User, username=username)
    
    # Fetch all addresses associated with this user
    addresses = Address.objects.filter(user=user)
    
    return render(request, 'extt/user_profile.html', {
        'user': user,
        'addresses': addresses,
    })


def update_username(request):
    if request.method == 'POST':
        form = UsernameUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your username has been updated successfully!')
            return redirect('user_profile', username=request.user.username)  # Redirect to the updated profile page
    else:
        form = UsernameUpdateForm(instance=request.user)
    
    return render(request, 'extt/update_username.html', {'form': form})

@login_required
def update_email(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)  # Redirect to the updated profile page
    else:
        form = EmailUpdateForm(instance=request.user)

    return render(request, 'extt/update_email.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Prevents logout after password change
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('login')  # Redirect to the user's profile page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'extt/change_password.html', {'form': form})

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user  # Link the address to the current user
            new_address.save()  # Save the new address
            
            return redirect('user_profile', username=request.user.username)  # Redirect to the user profile page or another page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AddressForm()

    return render(request, 'extt/add_address.html', {'form': form})


def add_new_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user  # Link the address to the current user
            new_address.save()  # Save the new address
            
            return redirect('checkout')  # Redirect to the user profile page or another page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AddressForm()

    return render(request, 'extt/add_new_address.html', {'form': form})


def edit_address(request, address_id):
    # Get the address by ID or return a 404 if not found
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        form = AddressEditForm(request.POST, instance=address)
        if form.is_valid():
            form.save()  # Save the updated address
            messages.success(request, 'Your address has been updated successfully.')
            return redirect('user_profile', username=request.user.username)  # Redirect to the user's profile or another page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AddressEditForm(instance=address)

    return render(request, 'extt/edit_address.html', {'form': form, 'address': address})

def remove_address(request, address_id):
    # Fetch the address by ID
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # Delete the address
    address.delete()
    
  
    
    return redirect('user_profile', username=request.user.username)  # Update this URL name as needed # Replace with the name of the address list view



def delivery_boy_home(request):
    # Get or create the DeliveryBoyStatus record for the logged-in user
    delivery_boy_status, created = DeliveryBoyStatus.objects.get_or_create(delivery_boy_update=request.user)

    return render(request, 'extt/delivery_boy_home.html', {
        'delivery_boy_status': delivery_boy_status,
    })

# Update the delivery boy's status (In/Out)
@login_required
def update_status(request, status):
    # Ensure the status is valid ('In' or 'Out')
    if status not in ['In', 'Out']:
        return redirect('delivery_boy_home')  # Redirect to home if status is invalid

    # Get or create the DeliveryBoyStatus record for the logged-in user
    delivery_boy_status, created = DeliveryBoyStatus.objects.get_or_create(delivery_boy_update=request.user)

    # Update the status
    delivery_boy_status.status = status
    delivery_boy_status.save()

    # Redirect back to the home page to reflect the status change
    return redirect('delivery_boy_home')


def assign_delivery_boy(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = AssignDeliveryBoyForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            
            return redirect('orders_list')  # Adjust this to the appropriate redirect
    else:
        form = AssignDeliveryBoyForm(instance=order)
    
    return render(request, 'extt/assign_delivery_boy.html', {'order': order, 'form': form})


def assigned_orders_list(request):
    orders = Order.objects.filter(delivery_boy_update=request.user).order_by('-created_at')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)

        if new_status in ['Order Placed', 'Pending', 'Shipped', 'Out for Delivery', 'Delivered']:
            order.status = new_status

            # Check if the status is changed to 'Delivered'
            if new_status == 'Delivered':
                order.delivered_at = timezone.now()  # Set the delivered_at time
                order.save()

                # Prepare the email content
                subject = 'Your Delivered Invoice - MEDMART'

                # Manually build the full URL using SITE_DOMAIN
                order_detail_url = f"{settings.SITE_DOMAIN}{reverse('order_detail', args=[order.id])}"

                # Render the email template with the order and user details
                html_content = render_to_string('extt/delivered_invoice.html', {
                    'user': order.user,
                    'order': order,
                    'order_items': order.order_items.all(),
                    'order_detail_url': order_detail_url,  # Pass the absolute URL
                })

                recipient_email = order.user.email

                # Send the email
                email = EmailMessage(
                    subject=subject,
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient_email],
                )
                email.content_subtype = 'html'  # Set email content type to HTML
                email.send(fail_silently=False)

            order.save()
        else:
            messages.error(request, "Invalid status.")

        return redirect('assigned_orders_list')

    return render(request, 'extt/assigned_orders_list.html', {'orders': orders})




def update_delivery_boy_location(request):
    if request.method == 'POST':
        print('location update')
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            status = data.get('status')

            if not (isinstance(latitude, (int, float)) and isinstance(longitude, (int, float))):
                return JsonResponse({'error': 'Invalid latitude or longitude.'}, status=400)

            if status != 'In':
                return JsonResponse({'error': 'Delivery boy must be "In" to update location.'}, status=400)

            delivery_boy_status, created = DeliveryBoyStatus.objects.get_or_create(delivery_boy_update=request.user)

            # Reverse geocoding to get address
            try:
                geolocator = Nominatim(user_agent="medmart_delivery_app")
                location = geolocator.reverse((latitude, longitude), language='en')
                address = location.address if location else "No address found"
            except Exception as e:
                address = f"Failed to fetch address: {str(e)}"

            # Update the status and location
            delivery_boy_status.status = status
            delivery_boy_status.latitude = latitude
            delivery_boy_status.longitude = longitude
            delivery_boy_status.location_name = address  # Ensure this field exists in your model
            delivery_boy_status.save()

            return JsonResponse({'message': 'Location updated successfully', 'address': address}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)



def delivery_boy_details(request):
    # Fetch all delivery boys' details
    delivery_boys = DeliveryBoyStatus.objects.all()

    # Render the page with the delivery boys' information
    return render(request, 'extt/delivery_boy_details.html', {'delivery_boys': delivery_boys})

def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


# Function to get coordinates from address
def get_coordinates(address):
    try:
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print("Failed to geocode the address.")
            return None, None
    except GeocoderTimedOut:
        print("Geocoding timed out. Try again later.")
        return None, None
    except GeocoderServiceError as e:
        print(f"Geocoding service error: {e}")
        return None, None




def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance in kilometers between two geographical points.
    """
    return geodesic((lat1, lon1), (lat2, lon2)).km


def get_live_distance(request, order_id):
    """
    API endpoint to fetch the live distance between the delivery boy and the order location.
    """
    order = get_object_or_404(Order, id=order_id)
    delivery_boy_status = DeliveryBoyStatus.objects.filter(
        delivery_boy_update=order.delivery_boy_update
    ).first()

    if not delivery_boy_status:
        return JsonResponse({'error': 'Delivery boy information is not available.'}, status=400)

    if order.latitude and order.longitude and delivery_boy_status.latitude and delivery_boy_status.longitude:
        distance = calculate_distance(
            delivery_boy_status.latitude,
            delivery_boy_status.longitude,
            order.latitude,
            order.longitude
        )
        return JsonResponse({'distance': distance}, status=200)
    else:
        return JsonResponse({'error': 'Coordinates are missing.'}, status=400)



def track_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    delivery_boy_status = DeliveryBoyStatus.objects.filter(
        delivery_boy_update=order.delivery_boy_update
    ).first()

    context = {
        'order': order,
        'delivery_boy': order.delivery_boy_update,
        'delivery_boy_status': delivery_boy_status,
    }
    return render(request, 'extt/track_delivery.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'extt/order_details.html', {'order': order})


def cart_item_count(request):
    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()  # Use CartItem, not Cart
    else:
        cart_items_count = 0
    return {'cart_items_count': cart_items_count}
