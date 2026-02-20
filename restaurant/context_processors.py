def order_count(request):
    order = request.session.get('order', {})
    count = 0
    for item in order.values():
        count += item.get('quantity', 0)
    
    is_staff = request.user.is_authenticated and (request.user.is_staff or request.user.groups.filter(name='Staff').exists())
    
    return {
        'order_count': count,
        'is_staff_member': is_staff
    }
