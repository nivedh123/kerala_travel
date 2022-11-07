
from django import forms
from .models import spot,reviewmodel,profilemodel
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  

class profileform(forms.ModelForm):
    class Meta:
        model=profilemodel
        fields=['Image','Name','Bio']
 
class searchFormbyDistrict(forms.Form):
    district=forms.CharField(max_length=20)

class reviewForm(forms.ModelForm):
    class Meta:
        model=reviewmodel
        fields=['content','rating']
class spotform(forms.ModelForm):
    class Meta:
        model=spot
        fields=['image','name','discription','link','district','type','warning']
   

   