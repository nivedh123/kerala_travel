
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
        widgets={'Bio':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 8}),
                'Bio_head':forms.Textarea(attrs={'class':'form-control','cols': 60, 'rows': 1}),
                'link':forms.widgets.URLInput(attrs={'class':'form-control'})}
                
class searchFormbyDistrict(forms.Form):
    district=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'formclass','placeholder':'search'}),max_length=50)


class reviewForm(forms.ModelForm):
    class Meta:
        model=reviewmodel
        fields=['content','rating','status']
        labels={'content':'write here','status':'did you visited the spot'}
        widgets={'content':forms.TextInput(attrs={'class':'form-control'}),
                'rating':forms.RadioSelect(attrs={'class':'radio-inline'}),
                'status':forms.RadioSelect(attrs={'class':'radio-inline'})}
class spotform(forms.ModelForm):
    class Meta:
        model=spot
        fields=['image','image2','image3','name','short_discription','discription','key_words','rel_link','link','district','type','warning']
        labels={'name':'Name of spot','short_discription':'discription title','discription':'discription',
                'key_words':'key words','rel_link':'referance','link':'location url'}
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                'short_discription':forms.TextInput(attrs={'class':'form-control'}),
                'discription':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 3}),
                'key_words':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 3}),
                'warning':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 3}),
                'rel_link':forms.widgets.URLInput(attrs={'class':'form-control'}),
                'district':forms.RadioSelect(attrs={'class':'radio-inline'}),
                'type':forms.RadioSelect(attrs={'class':'radio-inline'}),
                'link':forms.widgets.URLInput(attrs={'class':'form-control'}),}

   