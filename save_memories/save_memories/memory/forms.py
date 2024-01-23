from django import forms
from .models import Memory, Category
from django.forms import ModelForm, TextInput, Textarea, FileInput

class MemoryForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Выбрать категорию')
    new_category_name = forms.CharField(max_length=100, required=False, label='Или создать новую категорию')
    
    class Meta:
        model = Memory
        fields = [ 'title', 'description', 'image', 'category', 'new_category_name', 'latitude', 'longitude', 'address']

        labels = {
            'title': "",
            'description': "",
            'image': "Выберете изображение",
        }

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название Воспоминания'
                
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Полное Впечетление',
            }),
            'address': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(MemoryForm, self).__init__(*args, **kwargs)
            if user:
                self.fields['category'].queryset = Category.objects.filter(user=user)

        def clean(self):
            cleaned_data = super().clean()
            category = cleaned_data.get('category')
            new_category_name = cleaned_data.get('new_category_name')

            if not category and not new_category_name:
                raise forms.ValidationError("Выберите существующую категорию или укажите новую")

            return cleaned_data
        
        