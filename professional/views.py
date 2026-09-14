from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import Professional, Order
from customer.models import Customer


def professional_pending(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'professional'):
        return redirect('login')

    professional = request.user.professional

    if professional.status == 'Approved':
        return redirect('professional_home')

    return render(
        request,
        'professional/pending.html',
        {
            'professional': professional
        }
    )


@login_required(login_url='login')
def professional_home(request):

    if not hasattr(request.user, 'professional'):
        return redirect('login')

    professional = request.user.professional

    if professional.status != 'Approved':
        return redirect('professional_pending')

    orders = Order.objects.filter(
        professional=professional
    ).select_related(
        'customer'
    ).order_by('-created_at')

    pending_orders_count = Order.objects.filter(
        professional=professional,
        status='Pending'
    ).count()

    return render(
        request,
        'professional/home.html',
        {
            'professional': professional,
            'orders': orders,
            'pending_orders_count': pending_orders_count,
        }
    )


@login_required(login_url='login')
def update_order(request, order_id, action):

    if not hasattr(request.user, 'professional'):
        return redirect('login')

    professional = request.user.professional

    if professional.status != 'Approved':
        return redirect('professional_pending')

    order = get_object_or_404(
        Order,
        id=order_id,
        professional=professional
    )

    if order.status != 'Pending':
        return redirect('professional_home')

    if action == 'approve':
        order.status = 'Booked'
        order.save()

    elif action == 'reject':
        order.status = 'Rejected'
        order.save()

    return redirect('professional_home')


@login_required(login_url='login')
def professional_edit_profile(request):

    if not hasattr(request.user, 'professional'):
        return redirect('login')

    professional = request.user.professional

    if request.method == 'POST':

        professional.name = request.POST.get(
            'name',
            professional.name
        )

        professional.mobile = request.POST.get(
            'mobile',
            professional.mobile
        )

        professional.professional_type = request.POST.get(
            'professional_type',
            professional.professional_type
        )

        experience = request.POST.get('experience')

        if experience:
            professional.experience = experience

        professional.location = request.POST.get(
            'location',
            professional.location
        )

        hourly_charge = request.POST.get('hourly_charge')

        if hourly_charge:
            professional.hourly_charge = hourly_charge

        professional.save()

        return redirect('professional_home')

    return redirect('professional_home')


def professional_logout(request):
    logout(request)
    return redirect('login')