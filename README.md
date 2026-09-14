# ServeEase

**Find. Compare. Book.**

ServeEase is a Django-based local professional booking platform that connects customers with verified service professionals.

## Features

- Customer and Professional registration
- Admin approval workflow for professionals
- City and service-category based professional listings
- Booking and order management
- Professional approval/rejection of bookings
- Customer order status tracking
- Django Admin for administration

## Tech Stack

- Python
- Django 6.1.1
- HTML
- CSS
- JavaScript
- Bootstrap
- SQLite (local development)

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Security

The Django secret key is loaded from the `DJANGO_SECRET_KEY` environment variable. Do not commit production secrets, databases, passwords, or virtual environments.
