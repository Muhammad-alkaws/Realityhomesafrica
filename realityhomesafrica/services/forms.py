from django import forms
from .models import TradesmanProfile, PortfolioItem, ServiceRequest


class TradesmanProfileForm(forms.ModelForm):
    class Meta:
        model = TradesmanProfile
        fields = ['trade_category', 'years_experience', 'hourly_rate',
                  'location_city', 'location_state', 'certificate']
        widgets = {
            'years_experience': forms.NumberInput(attrs={'min': 0}),
            'hourly_rate': forms.NumberInput(attrs={'placeholder': 'e.g. 5000'}),
        }


class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ['title', 'description', 'image', 'completed_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['property_address', 'trade_needed', 'description']
        widgets = {
            'property_address': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the job needed...'}),
        }
