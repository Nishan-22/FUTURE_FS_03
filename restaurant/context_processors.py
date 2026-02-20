def cart_count(request):
    cart = request.session.get('cart', {})
    count = 0
    for item in cart.values():
        count += item.get('quantity', 0)
    return {'cart_count': count}
