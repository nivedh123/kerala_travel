
from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from ckeditor_uploader.fields import RichTextUploadingField 
#image compression method
def compress(image):
    im = Image.open(image)
    im = im.convert('RGB')
    im = im.resize((1920 ,1440), Image.ANTIALIAS)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image
def Compress(image):
    im = Image.open(image)
    im = im.convert('RGB')
    im = im.resize((400,400), Image.ANTIALIAS)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image


# Create your models here.
class districts(models.Model):
    district=models.CharField(max_length=20)
    image=models.ImageField(blank=True,null=True)
    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)
    def __str__(self):
        return self.district
class remark(models.Model):
    alert=models.CharField(max_length=20)
    image=models.ImageField(blank=True,null=True)
    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)
    def __str__(self):
        return self.alert

class profilemodel(models.Model):
    Image=models.ImageField()
    Bio_head=models.CharField(max_length=40,help_text='like PROFFESSIONAL PHOTOGRAPHER FOR 4 YEARS')
    Name=models.CharField(max_length=20)
    Bio=models.TextField()
    Date=models.DateTimeField(auto_now_add=True)
    link=models.URLField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profilemodel')
    verify=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        new_image = Compress(self.Image)
        self.Image = new_image
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.user)
class cluster(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(blank=True,null=True)
    publish=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class spot(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='spot')
    image=models.ImageField()
    ref_img=models.CharField(max_length=1000,blank=True,null=True)
    image2=models.ImageField(blank=True,null=True)
    ref_img2=models.CharField(max_length=1000,blank=True,null=True)
    image3=models.ImageField(blank=True,null=True)
    ref_img3=models.CharField(max_length=1000,blank=True,null=True)
    name=models.CharField(max_length=20,unique=True)
    short_discription=models.CharField(max_length=50,help_text='short title of your description',blank=True,null=True)
    discription=models.TextField()
    rel_link=models.URLField(help_text='you can add related articles link about place here',blank=True,null=True)
    link=models.URLField()
    district=models.ForeignKey(districts,on_delete=models.CASCADE)
    type=models.ForeignKey(remark,on_delete=models.CASCADE)
    warning=models.TextField(help_text='If you have any special advice for travellers give it here.',blank=True,null=True)
    key_words=models.TextField(help_text='Keywords are used to make your contribution more exposure in the search')
    cluster=models.ForeignKey(cluster,blank=True,null=True,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    verify=models.BooleanField(default=False)
    #rating=models.FloatField(default=5)
    class Meta:
        ordering=['district']
    def save(self, *args, **kwargs):
        self.name=self.name.upper()
        new_image = compress(self.image)
        self.image = new_image
        try:
            new_image2 = compress(self.image2)
            self.image2 = new_image2
        except:
            pass
        try:
            new_image3 = compress(self.image3)
            self.image3 = new_image3
        except:
            pass
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class reviewmodel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewmodel')
    content=models.TextField(blank=True,null=True)
    status=models.CharField(max_length=12,default='visited',choices=(('visited','visited'),('Not visited','Not visited')))
    rating=models.CharField(max_length=14,default='fentastic',choices=(('Below average','*'),('Average', '* *'),('Recomandable', '* * *'),('Good','* * * *'),('fentastic','* * * * *')))
    date=models.DateTimeField(auto_now_add=True)
    spot=models.ForeignKey(spot,on_delete=models.CASCADE,related_name='reviewmodel')


    def __str__(self):
        return str(self.spot)
    
