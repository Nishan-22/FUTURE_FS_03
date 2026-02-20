from django import forms
from .models import MenuItem, Category

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price', 'image', 'is_available']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'}),
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary', 'placeholder': 'Item Name'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary', 'rows': 4, 'placeholder': 'Item Description'}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-primary border-gray-300 rounded'}),
        }
