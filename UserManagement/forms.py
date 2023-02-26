from django import forms
from django.forms import ModelForm
from .models import Product, User

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['prd_name'].widget.attrs['class'] = 'form-control'
        self.fields['prd_desc'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['product_category'].widget.attrs['class'] = 'form-control'
        self.fields['product_image'].widget.attrs['class'] = 'form-control'

