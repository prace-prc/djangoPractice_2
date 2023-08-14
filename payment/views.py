from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        from django.urls import reverse
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        session_data = {'mode': 'payment',
                        'client_reference_id': order.id,
                        'success_url': success_url,
                        'cancel_url': cancel_url,
                        'line_items': []}
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())
