from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.models import Book
from .models import Cart, CartItem


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('home')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('book')

    for item in items:
        item.subtotal = item.book.price * item.quantity

    total = sum(item.book.price * item.quantity for item in items)

    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')