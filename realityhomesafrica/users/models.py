from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Extended User model for RealityHomesAfrica.
    Supports three roles: Client, Agent, Tradesman.
    """
    is_agent = models.BooleanField(default=False)
    is_tradesman = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def get_role(self):
        if self.is_agent:
            return "Agent"
        if self.is_tradesman:
            return "Tradesman"
        return "Client"

    def __str__(self):
        return f"{self.username} ({self.get_role()})"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    property_ref = models.ForeignKey(
        'listings.Property',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages'
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.subject}"
