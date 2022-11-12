
from django import forms
from .models import spot,reviewmodel,profilemodel
from django import forms  
from django.forms import Textarea
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class profileform(forms.ModelForm):
    class Meta:
        model=profilemodel
        fields=['Image','Name','Bio_head','Bio','link']
        labels={'Image':'profile Photo','Name':'Profile name','Bio_head':'title of your bio',
                'Bio':'bio','link':'Social media profile link'}
 
class searchFormbyDistrict(forms.Form):
    district=forms.CharField(label='',widget=forms.TextInput,max_length=50)


class reviewForm(forms.ModelForm):
    class Meta:
        model=reviewmodel
        fields=['content','rating','status']
        labels={'content':'write here','status':'did you visited the spot'}
class spotform(forms.ModelForm):
    class Meta:
        model=spot
        fields=['image','image2','image3','name','short_discription','discription','key_words','rel_link','link','district','type','warning']
        labels={'name':'Name of spot','short_discription':'discription title','discription':'discription',
                'key_words':'key words','rel_link':'referance','link':'location url'}
        widgets={'discription':Textarea(attrs={'cols': 80, 'rows': 3}),'warning':Textarea(attrs={'cols': 80, 'rows': 3}),}

   