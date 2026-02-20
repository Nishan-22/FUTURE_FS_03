from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from .models import Category, MenuItem, Order, OrderItem, Reservation, Review

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'category')
    search_fields = ('name', 'description')
    list_editable = ('is_available',)
    list_per_page = 20

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu_item', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_info', 'total_amount', 'status', 'order_date', 'custom_actions')
    list_filter = ('status', 'order_date')
    search_fields = ('customer_name', 'customer_email', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('order_date', 'total_amount', 'customer_name', 'customer_email', 'customer_phone')
    list_per_page = 20
    
    def customer_info(self, obj):
        if obj.user:
            return f"{obj.customer_name} (User: {obj.user.username})"
        return obj.customer_name
    customer_info.short_description = 'Customer'
    
    def custom_actions(self, obj):
        if obj.status == 'Pending':
            return format_html(
                '<a class="button" href="{}" style="padding: 5px 10px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 3px;">Process Order</a>',
                reverse('admin:restaurant_order_process', args=[obj.id])
            )
        elif obj.status == 'Processing':
            return format_html(
                '<a class="button" href="{}" style="padding: 5px 10px; background-color: #2196F3; color: white; text-decoration: none; border-radius: 3px;">Complete Order</a>',
                reverse('admin:restaurant_order_complete', args=[obj.id])
            )
        return 'Order Complete'
    custom_actions.short_description = 'Actions'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/process/', self.admin_site.admin_view(self.process_order), name='restaurant_order_process'),
            path('<int:order_id>/complete/', self.admin_site.admin_view(self.complete_order), name='restaurant_order_complete'),
        ]
        return custom_urls + urls
    
    def process_order(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order.status == 'Pending':
            order.status = 'Processing'
            order.save()
            messages.success(request, f'Order #{order.id} is now being processed.')
        else:
            messages.error(request, 'Order cannot be processed at this stage.')
        return HttpResponseRedirect(reverse('admin:restaurant_order_changelist'))
    
    def complete_order(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order.status == 'Processing':
            order.status = 'Completed'
            order.save()
            messages.success(request, f'Order #{order.id} has been completed.')
        else:
            messages.error(request, 'Order cannot be completed at this stage.')
        return HttpResponseRedirect(reverse('admin:restaurant_order_changelist'))

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date', 'time', 'number_of_guests', 'confirmed', 'confirmation_action')
    list_filter = ('confirmed', 'date')
    search_fields = ('name', 'email', 'phone')
    list_editable = ('confirmed',)
    list_per_page = 20
    
    def confirmation_action(self, obj):
        if not obj.confirmed:
            return format_html(
                '<a class="button" href="{}" style="padding: 5px 10px; background-color: #FF9800; color: white; text-decoration: none; border-radius: 3px;">Confirm</a>',
                reverse('admin:restaurant_reservation_confirm', args=[obj.id])
            )
        return 'Confirmed'
    confirmation_action.short_description = 'Action'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:reservation_id>/confirm/', self.admin_site.admin_view(self.confirm_reservation), name='restaurant_reservation_confirm'),
        ]
        return custom_urls + urls
    
    def confirm_reservation(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if not reservation.confirmed:
            reservation.confirmed = True
            reservation.save()
            messages.success(request, f'Reservation for {reservation.name} has been confirmed.')
        else:
            messages.info(request, 'Reservation was already confirmed.')
        return HttpResponseRedirect(reverse('admin:restaurant_reservation_changelist'))

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'user', 'rating', 'created_at', 'short_comment')
    list_filter = ('rating', 'created_at')
    search_fields = ('menu_item__name', 'user__username', 'comment')
    list_per_page = 20
    
    def short_comment(self, obj):
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return 'No comment'
    short_comment.short_description = 'Comment'

# Register models with enhanced admin
admin.site.register(Category)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review, ReviewAdmin)