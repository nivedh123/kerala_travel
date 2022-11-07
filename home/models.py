from email.policy import default
from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from io import BytesIO
from PIL import Image
from django.core.files import File

#image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image



# Create your models here.
class districts(models.Model):
    district=models.CharField(max_length=20)
    def __str__(self):
        return self.district
class remark(models.Model):
    alert=models.CharField(max_length=20)
    def __str__(self):
        return self.alert

class profilemodel(models.Model):
    Image=models.ImageField('profile/')
    Name=models.CharField(max_length=20)
    Bio=models.TextField()
    Date=models.DateTimeField(auto_now_add=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profilemodel')
    verify=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        new_image = compress(self.Image)
        self.image = new_image
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.Name)

class spot(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='spot')
    image=models.ImageField()
    name=models.CharField(max_length=20)
    discription=models.TextField()
    link=models.URLField()
    district=models.ForeignKey(districts,on_delete=models.CASCADE)
    type=models.ForeignKey(remark,on_delete=models.CASCADE)
    warning=models.TextField()
    verify=models.BooleanField(default=False)
    

    #rating=models.FloatField(default=5)
    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)
       

    def __str__(self):
        return self.name


class reviewmodel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewmodel')
    content=models.TextField()
    rating=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    date=models.DateTimeField(auto_now_add=True)
    spot=models.ForeignKey(spot,on_delete=models.CASCADE,related_name='reviewmodel')
    def __str__(self):
        return str(self.spot)
    
