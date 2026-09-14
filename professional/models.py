from django.db import models
from django.contrib.auth.models import User


class Professional(models.Model):

    PROFESSIONAL_TYPES = [
        ('Carpenter', 'Carpenter'),
        ('Electrician', 'Electrician'),
        ('AC Technician', 'AC Technician'),
        ('Mechanic', 'Mechanic'),
        ('Plumber', 'Plumber'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    mobile = models.CharField(
        max_length=15
    )

    professional_type = models.CharField(
        max_length=50,
        choices=PROFESSIONAL_TYPES
    )

    experience = models.PositiveIntegerField()

    location = models.CharField(
        max_length=100
    )

    hourly_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    profile_image = models.CharField(
        max_length=500,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return self.name


class Order(models.Model):

    TIME_SLOTS = [
        ('8-10 AM', '8-10 AM'),
        ('10-12 PM', '10-12 PM'),
        ('12-2 PM', '12-2 PM'),
        ('2-4 PM', '2-4 PM'),
        ('4-6 PM', '4-6 PM'),
        ('6-8 PM', '6-8 PM'),
    ]

    LANGUAGE_CHOICES = [
        ('Tamil', 'Tamil'),
        ('English', 'English'),
        ('Hindi', 'Hindi'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Booked', 'Booked'),
        ('Rejected', 'Rejected'),
    ]

    customer = models.ForeignKey(
        'customer.Customer',
        on_delete=models.CASCADE
    )

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE
    )

    booking_date = models.DateField()

    time_slot = models.CharField(
        max_length=20,
        choices=TIME_SLOTS
    )

    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'{self.customer.name} - '
            f'{self.professional.name}'
        )