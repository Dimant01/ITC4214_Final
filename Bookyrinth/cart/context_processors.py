from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            count = sum(item.quantity for item in cart.items.all())
        else:
            count = 0
    else:
        count = 0

    return {
        'cart_count': count
    }