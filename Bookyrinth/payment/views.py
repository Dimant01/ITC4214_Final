from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, Book
from .forms import CheckoutForm
from django.db import transaction
from django.contrib import messages
from accounts.models import UserActivity

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

            with transaction.atomic():

                # 1. STOCK VALIDATION
                for item in items:
                    if item.quantity > item.book.stock:
                        messages.error(
                            request,
                            f"Not enough stock for '{item.book.title}'. Please update your cart."
                        )
                        return redirect('cart')

                # 2. REDUCE STOCK
                for item in items:
                    book = item.book
                    book.stock -= item.quantity
                    book.save()

                # 3. SUCCESS MESSAGE
                messages.success(request, "Payment successful! Your order has been placed.")

                # 4. CLEAR CART
                cart.items.all().delete()

                for item in items:
                    UserActivity.objects.create(
                    user=request.user,
                    book=item.book,
                    activity_type="purchase"
                )

            return redirect('payment_success')

        else:
            messages.error(request, "Please correct the errors in the form.")

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