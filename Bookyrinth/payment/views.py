from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart

# Create your views here.

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.select_related('book')

    total = sum(item.book.price * item.quantity for item in items)

    if request.method == "POST":
        # simulate payment success
        cart.items.all().delete()  # clear cart
        return redirect('payment_success')

    return render(request, 'payment/checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def success(request):
    return render(request, 'payment/success.html')

@login_required
def cancel_payment(request):
    return redirect('cart')