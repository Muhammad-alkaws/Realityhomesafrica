from django.db import models
from django.conf import settings


TRADE_CATEGORIES = [
    ('plumber', 'Plumber'),
    ('electrician', 'Electrician'),
    ('painter', 'Painter'),
    ('carpenter', 'Carpenter'),
    ('mason', 'Mason'),
    ('tiler', 'Tiler'),
    ('ac_technician', 'AC Technician'),
    ('other', 'Other'),
]

SERVICE_STATUS = [
    ('open', 'Open'),
    ('accepted', 'Accepted'),
    ('completed', 'Completed'),
]


class TradesmanProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tradesman_profile'
    )
    trade_category = models.CharField(max_length=30, choices=TRADE_CATEGORIES)
    years_experience = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    location_city = models.CharField(max_length=100, blank=True)
    location_state = models.CharField(max_length=100, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_trade_category_display()}"


class PortfolioItem(models.Model):
    tradesman = models.ForeignKey(TradesmanProfile, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio/%Y/%m/')
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class ServiceRequest(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    tradesman = models.ForeignKey(TradesmanProfile, on_delete=models.CASCADE, related_name='requests')
    property_address = models.TextField()
    trade_needed = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=SERVICE_STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.client.username} to {self.tradesman.user.username}"
