from django.contrib import admin
from django.contrib import messages

from .models import Professional, Order


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'mobile',
        'professional_type',
        'experience',
        'location',
        'hourly_charge',
        'status',
    )

    list_filter = (
        'status',
        'professional_type',
        'location',
    )

    search_fields = (
        'name',
        'mobile',
        'location',
    )

    actions = [
        'approve_professionals',
        'reject_professionals',
    ]

    @admin.action(
        description='Approve selected professionals'
    )
    def approve_professionals(
        self,
        request,
        queryset
    ):

        updated = queryset.filter(
            status='Pending'
        ).update(
            status='Approved'
        )

        self.message_user(
            request,
            f'{updated} professional(s) approved.',
            messages.SUCCESS
        )

    @admin.action(
        description='Reject selected professionals'
    )
    def reject_professionals(
        self,
        request,
        queryset
    ):

        professionals = queryset.filter(
            status='Pending'
        )

        count = professionals.count()

        for professional in professionals:

            user = professional.user

            professional.delete()
            user.delete()

        self.message_user(
            request,
            f'{count} professional(s) rejected and deleted.',
            messages.WARNING
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'customer_name',
        'professional_name',
        'location',
        'booking_date',
        'time_slot',
        'status',
    )

    list_filter = (
        'status',
        'booking_date',
        'time_slot',
    )

    search_fields = (
        'customer__name',
        'professional__name',
        'professional__location',
    )

    def customer_name(self, obj):
        return obj.customer.name

    customer_name.short_description = 'Customer Name'

    def professional_name(self, obj):
        return obj.professional.name

    professional_name.short_description = 'Professional Name'

    def location(self, obj):
        return obj.professional.location

    location.short_description = 'Location'