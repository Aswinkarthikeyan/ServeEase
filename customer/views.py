from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import JsonResponse

from .models import Customer
from professional.models import Professional, Order


def register(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        account_type = request.POST.get('account_type')

        if not all([
            name,
            mobile,
            password,
            confirm_password,
            account_type
        ]):
            return render(
                request,
                'customer/register.html',
                {
                    'error': 'Please fill all required fields.'
                }
            )

        if password != confirm_password:
            return render(
                request,
                'customer/register.html',
                {
                    'error': 'Passwords do not match.'
                }
            )

        if User.objects.filter(username=mobile).exists():
            return render(
                request,
                'customer/register.html',
                {
                    'error': 'This mobile number is already registered.'
                }
            )

        user = User.objects.create_user(
            username=mobile,
            password=password
        )

        if account_type == 'Customer':

            Customer.objects.create(
                user=user,
                name=name,
                mobile=mobile
            )

            return redirect('login')


        if account_type == 'Professional':

            professional_type = request.POST.get(
                'professional_type'
            )

            experience = request.POST.get(
                'experience'
            )

            location = request.POST.get(
                'location'
            )

            hourly_charge = request.POST.get(
                'hourly_charge'
            )

            if not all([
                professional_type,
                experience,
                location,
                hourly_charge
            ]):

                user.delete()

                return render(
                    request,
                    'customer/register.html',
                    {
                        'error':
                        'Please fill all professional details.'
                    }
                )


            Professional.objects.create(

                user=user,

                name=name,

                mobile=mobile,

                professional_type=professional_type,

                experience=experience,

                location=location,

                hourly_charge=hourly_charge,

                status='Pending'

            )

            return redirect('login')


        user.delete()

        return render(
            request,
            'customer/register.html',
            {
                'error': 'Invalid account type.'
            }
        )


    return render(
        request,
        'customer/register.html'
    )


def customer_login(request):

    if request.method == 'POST':

        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=mobile,
            password=password
        )

        if user is None:

            return render(
                request,
                'customer/login.html',
                {
                    'error':
                    'Invalid mobile number or password.'
                }
            )


        login(request, user)


        if hasattr(user, 'professional'):

            professional = user.professional

            if professional.status == 'Pending':
                return redirect('professional_pending')

            if professional.status == 'Approved':
                return redirect('professional_home')


        if hasattr(user, 'customer'):
            return redirect('customer_home')


        logout(request)

        return render(
            request,
            'customer/login.html',
            {
                'error': 'Invalid account.'
            }
        )


    return render(
        request,
        'customer/login.html'
    )


def customer_home(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'customer'):
        return redirect('login')


    professionals = Professional.objects.filter(
        status='Approved'
    )


    selected_city = request.GET.get('city')
    selected_service = request.GET.get('service')


    if selected_city:

        professionals = professionals.filter(
            location__iexact=selected_city
        )


    if selected_service:

        professionals = professionals.filter(
            professional_type=selected_service
        )


    professionals = professionals.order_by(
        'professional_type',
        'name'
    )


    customer_orders = Order.objects.filter(
        customer=request.user.customer
    ).select_related(
        'professional'
    ).order_by(
        '-created_at'
    )


    return render(
        request,
        'customer/home.html',
        {
            'professionals': professionals,

            'selected_city': selected_city,

            'selected_service': selected_service,

            'customer_orders': customer_orders,
        }
    )


def get_booked_slots(request):

    professional_id = request.GET.get(
        'professional_id'
    )

    booking_date = request.GET.get(
        'booking_date'
    )


    if not professional_id or not booking_date:

        return JsonResponse(
            {
                'booked_slots': []
            }
        )


    booked_slots = Order.objects.filter(

        professional_id=professional_id,

        booking_date=booking_date,

        status__in=[
            'Pending',
            'Booked'
        ]

    ).values_list(
        'time_slot',
        flat=True
    )


    return JsonResponse(
        {
            'booked_slots': list(booked_slots)
        }
    )


def create_order(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'customer'):
        return redirect('login')


    if request.method != 'POST':
        return redirect('customer_home')


    professional_id = request.POST.get(
        'professional_id'
    )

    booking_date = request.POST.get(
        'booking_date'
    )

    time_slot = request.POST.get(
        'time_slot'
    )

    language = request.POST.get(
        'language'
    )


    if not all([
        professional_id,
        booking_date,
        time_slot,
        language
    ]):

        return redirect('customer_home')


    professional = get_object_or_404(

        Professional,

        id=professional_id,

        status='Approved'

    )


    try:

        selected_date = timezone.datetime.strptime(
            booking_date,
            '%Y-%m-%d'
        ).date()

    except ValueError:

        return redirect('customer_home')


    today = timezone.localdate()


    # No same-day booking.

    if selected_date <= today:

        return redirect('customer_home')


    # Backend duplicate protection.

    slot_taken = Order.objects.filter(

        professional=professional,

        booking_date=selected_date,

        time_slot=time_slot,

        status__in=[
            'Pending',
            'Booked'
        ]

    ).exists()


    if slot_taken:

        return redirect('customer_home')


    Order.objects.create(

        customer=request.user.customer,

        professional=professional,

        booking_date=selected_date,

        time_slot=time_slot,

        language=language,

        status='Pending'

    )


    return redirect('customer_home')


def customer_edit_profile(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'customer'):
        return redirect('login')


    customer = request.user.customer


    if request.method == 'POST':

        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        if name:
            customer.name = name

        if mobile and mobile != customer.mobile:

            if User.objects.filter(
                username=mobile
            ).exclude(
                id=request.user.id
            ).exists():

                return redirect('customer_home')


            request.user.username = mobile
            request.user.save()

            customer.mobile = mobile


        customer.save()


    return redirect('customer_home')


def customer_logout(request):

    logout(request)

    return redirect('login')