


from django import forms
from .models import reviewmodel_blog,blogmodel
from django import forms  
from django.forms import Textarea
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from ckeditor.widgets import CKEditorWidget

class blogform(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model=blogmodel
        fields=['title','image1','image2','place','date_travel','content','keywords']
        labels={'title':'Name of travel document','image2':'image2 (optional)','place':'place(optional)','date_travel':'date of travel(optional)','content':'body'}
        widgets={'title':forms.TextInput(attrs={'class':"form-control"}),
                'place':forms.TextInput(attrs={'class':"form-control"}),
                'date_travel':forms.SelectDateWidget(years=range(1980, 2025)),
                'keywords':Textarea(attrs={'class':'form-control','cols': 60, 'rows': 3,'placeholder':'give spaces between keywords, eg: fishing beach evening sunset ...'}),
                }

class reviewForm(forms.ModelForm):
    class Meta:
        model=reviewmodel_blog
        fields=['content']
        labels={
                'content':''}
        widgets={'content':forms.Textarea(attrs={'class':"form-control animated",'style':'color:white;background-color:  rgb(80, 38, 38);','cols':"50",'placeholder':'Enter your review here...', 'rows':'5'})}