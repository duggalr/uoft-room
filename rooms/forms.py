from django import forms
from .models import TestingImage


# Create your forms here.
class ImageForm(forms.ModelForm):
  image = forms.ImageField(label='Image')
  class Meta:
    model = TestingImage
    fields = ('image', 'person_name')
  


