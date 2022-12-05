from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image
from django.core.files import File
from ckeditor.fields import RichTextField
from home.models import spot,profilemodel
from datetime import date
#image compression method
def compress(image):
    im = Image.open(image)
    im = im.convert('RGB')
    im = im.resize((1920 ,1440), Image.ANTIALIAS)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image
# Create your models here.
class blogmodel(models.Model):
    image1=models.ImageField()
    image2=models.ImageField(blank=True,null=True)
    place=models.CharField(max_length=60,blank=True,null=True)
    date_travel=models.DateField(blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogmodel')
    title=models.CharField(max_length=150)
    content=RichTextField()
    date=models.DateTimeField(auto_now_add=True)
    verify=models.BooleanField(default=True)
    keywords=models.TextField(blank=True,null=True)
    def save(self, *args, **kwargs):
        new_image = compress(self.image1)
        self.image1 = new_image
        new_image = compress(self.image2)
        self.image2 = new_image
        super().save(*args, **kwargs)
class reviewmodel_blog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewmodel_blog')
    content=models.TextField(blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)
    spot=models.ForeignKey(blogmodel,on_delete=models.CASCADE,related_name='reviewmodel_blog')


    def __str__(self):
        return str(self.spot)