from django.shortcuts import render, get_object_or_404
from .models import Phone, Customer, CustomerOrder
from .forms import PhoneForm, UpdateStockForm
from django.shortcuts import redirect
from .forms import CustomerForm
from django.contrib import messages
from .models import CustomerOrder
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum, F
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.
def home(request):
    return render(request, 'store/home.html')

def phone_list(request):
    phones = Phone.objects.all()
    return render(request, 'store/phone_list.html', {'phones': phones})

def phone_detail(request, phone_id):
    phone = get_object_or_404(Phone, pk=phone_id)
    return render(request, 'store/phone_detail.html', {'phone': phone})

def add_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Phone added successfully!")
            return redirect('phone_list')
    else:
        form = PhoneForm()
    return render(request, 'store/add_phone.html', {'form': form})

def edit_phone(request, phone_id):
    phone = get_object_or_404(Phone, pk=phone_id)
    if request.method == 'POST':
        form = PhoneForm(request.POST, request.FILES, instance=phone)
        if form.is_valid():
            form.save()
            messages.success(request, "Phone updated successfully!")
            return redirect('phone_list')
    else:
        form = PhoneForm(instance=phone)
    return render(request, 'store/edit_phone.html', {'form': form, 'phone': phone})

def delete_phone(request, phone_id):
    phone = get_object_or_404(Phone, pk=phone_id)
    if request.method == 'POST':
        phone.delete()
        messages.success(request, "Phone deleted successfully.")
        return redirect('phone_list')
    return render(request, 'store/delete_phone.html', {'phone': phone})

def buy_phone(request):
    phones = Phone.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_id = request.POST['phone_bought']
        payment_method = request.POST['payment_method']
        phone = Phone.objects.get(id=phone_id)

        # Check if phone is in stock
        if phone.stock > 0:
            # Create customer order
            Customer.objects.create(
                name=name,
                email=email,
                phone_bought=phone,
                payment_method=payment_method
            )

            # Decrease stock by 1
            phone.stock -= 1
            phone.save()

            messages.success(request, f'{phone.name} bought successfully!')
        else:
            messages.error(request, 'Sorry, this phone is out of stock!')

        return redirect('home')

    return render(request, 'store/buy_phone.html', {'phones': phones})

def customer_orders(request):
    payment_method = request.GET.get('payment_method')
    
    if payment_method:
        customers = Customer.objects.filter(payment_method=payment_method)
    else:
        customers = Customer.objects.all()

    return render(request, 'store/customer_orders.html', {
        'customers': customers,
        'selected_payment': payment_method
    })


def update_stock(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)

    if request.method == 'POST':
        form = UpdateStockForm(request.POST, instance=phone)
        if form.is_valid():
            form.save()
            messages.success(request, f'Stock for {phone.name} updated successfully!')
            return redirect('phone_list')
    else:
        form = UpdateStockForm(instance=phone)

    return render(request, 'store/update_stock.html', {'form': form, 'phone': phone})

def filter_orders_by_payment(request):
    payment_method = request.GET.get('payment_method', 'on_the_spot')  # Default filter is 'on_the_spot'
    orders = CustomerOrder.objects.filter(payment_method=payment_method)
    return render(request, 'store/order_list_filtered.html', {'orders': orders, 'payment_method': payment_method})

def customer_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer_orders = Customer.objects.filter(email=customer.email)  # in case same person bought multiple times

    return render(request, 'store/customer_profile.html', {
        'customer': customer,
        'orders': customer_orders
    })
def sales_dashboard(request):
    from django.db.models.functions import TruncMonth
    from django.db.models import Sum, Count

    # Total sales revenue
    total_sales = Customer.objects.aggregate(total=Sum('phone_bought__price'))['total'] or 0

    # Sales by month
    sales_by_month = Customer.objects.annotate(month=TruncMonth('date_bought')).values('month').annotate(
        total=Sum('phone_bought__price')
    ).order_by('month')

    # Most popular phone
    popular_phone = Customer.objects.values('phone_bought__name').annotate(
        count=Count('id')
    ).order_by('-count').first()

    # Total phones sold
    total_phones_sold = Customer.objects.count()

    # Top earning phone
    top_earning = Customer.objects.values('phone_bought__name').annotate(
        revenue=Sum('phone_bought__price')
    ).order_by('-revenue').first()

    context = {
        'total_sales': total_sales,
        'sales_by_month': sales_by_month,
        'popular_phone': popular_phone,
        'total_phones_sold': total_phones_sold,
        'top_earning': top_earning,
    }
    return render(request, 'store/sales_dashboard.html', context)


@csrf_exempt
def upc_lookup(request):
    product = None
    error = None

    if request.method == 'POST':
        upc_code = request.POST.get('upc')

        if upc_code:
            api_url = f'https://api.upcitemdb.com/prod/trial/lookup?upc={upc_code}'

            try:
                response = requests.get(api_url)
                data = response.json()

                if data.get('code') == 'OK' and data.get('total') > 0:
                    product = data['items'][0]
                else:
                    error = 'Product not found.'
            except Exception as e:
                error = f'Error fetching data: {e}'
        else:
            error = 'Please enter a UPC code.'

    return render(request, 'store/upc_lookup.html', {'product': product, 'error': error})