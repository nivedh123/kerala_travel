from django.db import models
from django.contrib.auth.models import User
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
class blogmodel(models.Model):
    image1=models.ImageField()
    image2=models.ImageField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogmodel')
    title=models.CharField(max_length=150)
    content=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)

class reviewmodel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewmodel')
    content=models.TextField()
    rating=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    date=models.DateTimeField(auto_now_add=True)
    blogmodel=models.ForeignKey(blogmodel,on_delete=models.CASCADE,related_name='reviewmodel')
    def __str__(self):
        return str(self.spot)