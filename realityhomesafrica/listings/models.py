from django.db import models
from django.conf import settings


PROPERTY_TYPES = [
    ('land', 'Land'),
    ('flat', 'Flat / Apartment'),
    ('bungalow', 'Bungalow'),
    ('duplex', 'Duplex'),
    ('commercial', 'Commercial'),
]

INSPECTION_STATUS = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
]

NIGERIAN_STATES = [
    ('Abuja', 'Abuja (FCT)'),
    ('Lagos', 'Lagos'),
    ('Rivers', 'Rivers'),
    ('Kano', 'Kano'),
    ('Oyo', 'Oyo'),
    ('Kaduna', 'Kaduna'),
    ('Enugu', 'Enugu'),
    ('Delta', 'Delta'),
    ('Ogun', 'Ogun'),
    ('Anambra', 'Anambra'),
    ('Other', 'Other'),
]


class Property(models.Model):
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=NIGERIAN_STATES, default='Abuja')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='flat')
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} - {self.city}"

    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image.url
        first = self.images.first()
        return first.image.url if first else None

    def format_price(self):
        return "N{:,.0f}".format(self.price)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class Inspection(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inspections')
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_inspections'
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agent_inspections'
    )
    requested_date = models.DateTimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=INSPECTION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection: {self.client.username} > {self.property.title} ({self.status})"


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} fav {self.property.title}"
