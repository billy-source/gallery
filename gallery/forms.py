from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter photo title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter photo description',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-gray-700 text-white border border-gray-600 file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-2 file:rounded-md hover:file:bg-blue-600'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Add tags (comma separated)'
            }),
        }
