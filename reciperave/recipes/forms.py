from django import forms
from .models import Recipe, Category

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'total_time', 'dishType', 'description', 'photo_video', 'instruction']
    
    # You can override the __init__ method if you need to set choices dynamically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dishType'].widget = forms.Select(choices=[(cat.dishtype, cat.dishtype) for cat in Category.objects.all()])