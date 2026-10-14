from django import forms
from .models import Property, PropertyImage, Inspection

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
MAX_IMAGE_SIZE_MB = 5


def validate_image(image):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise forms.ValidationError("Only JPG, PNG, or WEBP images are allowed.")
    if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise forms.ValidationError(f"Image must be under {MAX_IMAGE_SIZE_MB}MB.")


class PropertyForm(forms.ModelForm):
    # Extra: allow uploading multiple images at once
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        required=False,
        label="Property Images"
    )
    primary_image = forms.ImageField(required=False, label="Primary / Cover Image")

    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'address', 'city', 'state',
            'property_type', 'bedrooms', 'bathrooms', 'is_available',
            'latitude', 'longitude',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'price': forms.NumberInput(attrs={'placeholder': 'e.g. 25000000'}),
        }


class InspectionRequestForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['requested_date', 'message']
        widgets = {
            'requested_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests?'}),
        }
