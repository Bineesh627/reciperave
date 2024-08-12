from django import forms
from .models import Recipe, Category

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'total_time', 'dishType', 'description', 'photo', 'video', 'instruction']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dishType'].widget = forms.Select(choices=[(cat.dishtype, cat.dishtype) for cat in Category.objects.all()])
