from django import forms
from .models import Score

# class UploadForm(forms.Form):
class UploadForm(forms.ModelForm):
   
    class Meta:
        model = Score
        fields =  ['name', 'choice', 'name_sub'] 
        # widgets = {
        #     'choice': forms.widgets.CheckboxSelectMultiple, 
        # }

