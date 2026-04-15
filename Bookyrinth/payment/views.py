from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .forms import CheckoutForm

#Create your views here

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.select_related('book')

    for item in items:
        item.subtotal = item.book.price * item.quantity

    total = sum(item.subtotal for item in items)

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Example: extracted data
            address = data["address"]
            city = data["city"]
            postal_code = data["postal_code"]
            payment_method = data["payment_method"]

            # simulate payment
            print(address, city, postal_code, payment_method)

            cart.items.all().delete()
            return redirect('payment_success')

    else:
        form = CheckoutForm()

    return render(request, 'payment/checkout.html', {
        'items': items,
        'total': total,
        'form': form
    })

@login_required 
def success(request): 
    return render(request, 'payment/success.html') 

@login_required 
def cancel_payment(request):
    return redirect('cart')