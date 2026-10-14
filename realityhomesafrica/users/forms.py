from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Message


class ClientRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        user.is_agent = False
        user.is_tradesman = False
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        if commit:
            user.save()
        return user


class AgentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False,
                          help_text="Tell clients about your experience")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'bio', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_agent = True
        user.is_client = False
        user.is_tradesman = False
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.bio = self.cleaned_data.get('bio', '')
        if commit:
            user.save()
        return user


class TradesmanRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tradesman = True
        user.is_client = False
        user.is_agent = False
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}),
        }
