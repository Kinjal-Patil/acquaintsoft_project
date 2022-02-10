from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your forms here.
from products.models import Products, Category


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProductForm(forms.ModelForm):
    manufacturing_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    expiry_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Products
        fields = ("category", "product_name", "product_code", "price", "manufacturing_date", "expiry_date")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
