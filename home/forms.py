
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
    district=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'formclass','placeholder':'search','placeholder':'eg:kozhikode beach'}),max_length=50)


class reviewForm(forms.ModelForm):
    class Meta:
        model=reviewmodel
        fields=['content','rating','status']
        labels={'status':'status',
                'rating':'rate',
                'content':''}
        widgets={'content':forms.Textarea(attrs={'class':"form-control animated",'style':'color:white;background-color:  rgb(80, 38, 38);','cols':"50",'placeholder':'Enter your review here...', 'rows':'5'}),
                'rating':forms.Select(attrs={'style':'background-color:  rgb(80, 38, 38);color:white;'}),
                'status':forms.Select(attrs={'style':'background-color:  rgb(80, 38, 38);color:white;'})}
class spotform(forms.ModelForm):
    class Meta:
        model=spot
        fields=['image','ref_img','image2','ref_img2','image3','ref_img3','name','short_discription','discription','key_words','rel_link','link','district','type','warning']
        labels={'image2':'image (optional)','ref_img':'mention image owner','ref_img2':'mention image owner','ref_img3':'mention image owner','image3':'image (optional)','name':'Name of spot','short_discription':'discription title','discription':'discription',
                'key_words':'key words','rel_link':'referance','link':'location url'}
        widgets={'ref_img':forms.TextInput(attrs={'class':'form-control','placeholder':'If the image is not yours, give a shoutout to the owner'}),
                'ref_img2':forms.TextInput(attrs={'class':'form-control','placeholder':'If the image is not yours, give a shoutout to the owner'}),
                'ref_img3':forms.TextInput(attrs={'class':'form-control','placeholder':'If the image is not yours, give a shoutout to the owner'}),
                'name':forms.TextInput(attrs={'class':'form-control','placeholder':'eg:Kozhikode beach'}),
                'short_discription':forms.TextInput(attrs={'class':'form-control','placeholder':'eg:Kozhikode beach or calicut beach'}),
                'discription':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 3,'placeholder':'if you taking a description from any other source kindly mention its source also(Hyperlinks supported)'}),
                'key_words':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 3,'placeholder':'give spaces between keywords, eg: fishing beach evening sunset ...'}),
                'warning':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 3,'placeholder':"visitor's time is between 8.00 am to 6.00 pm, Slippery rocks are present be careful, not look good for family travels, Sunset view is more good here, and travelling on a two-wheeler is more comfortable in this place."}),
                'rel_link':forms.widgets.URLInput(attrs={'class':'form-control','placeholder':'must be url'}),
                'district':forms.RadioSelect(attrs={'class':'radio-inline',}),
                'type':forms.RadioSelect(attrs={'class':'radio-inline',}),
                'link':forms.widgets.URLInput(attrs={'class':'form-control','placeholder':'google map location url'})}

   