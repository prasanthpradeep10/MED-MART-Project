
from django import forms
from .models import Address
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Category,Product,Rating1,Order

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


class CheckoutForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=True,
        label="Select Address",
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user=user)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating1
        fields = ['rating', ]

class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']  # Only include the username field

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if the username is already taken by another user
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
    

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']  # Only include the email field

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email is already taken by another user
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        }),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a new password'
        }),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter the new password'
        }),
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        # Ensure passwords match
        if new_password1 != new_password2:
            raise ValidationError("The two password fields didn't match.")

        return cleaned_data

    


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'city', 'state', 'postal_code', 'country', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, customize widgets for better form appearance
        self.fields['address_line'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['city'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['state'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['postal_code'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['country'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['is_default'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'}) 


class AddressEditForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'city', 'state', 'postal_code', 'country', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, customize widgets for better form appearance
        self.fields['address_line'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['city'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['state'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['postal_code'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['country'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['is_default'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})   


    

class AssignDeliveryBoyForm(forms.ModelForm):
    delivery_boy_update = forms.ModelChoiceField(
        queryset=User.objects.filter(deliveryboystatus__status='In'),  # Use the correct related name
        required=True,
        label="Assign Delivery Boy"
    )

    class Meta:
        model = Order
        fields = ['delivery_boy_update']

   