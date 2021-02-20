from django import forms
from .models import  Listing, Categories, User

class create_page(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title','description','starting_bid','category','image')
        widgets = {
            'title':  forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.TextInput(attrs={'class':'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class':'form-control'}),
            'category': forms.Select(choices = Categories.objects.all(),attrs={'class':'form-control'}),
            'image': forms.TextInput(attrs={'class':'form-control', 'max_length': 200})
        }
