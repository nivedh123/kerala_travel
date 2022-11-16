
from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

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

class spot(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='spot')
    image=models.ImageField()
    image2=models.ImageField(blank=True,null=True)
    image3=models.ImageField(blank=True,null=True)
    name=models.CharField(max_length=20)
    short_discription=models.CharField(max_length=50,help_text='short description place in 50 words')
    discription=models.TextField()
    rel_link=models.URLField(help_text='you can add related articles link about place here',default='https://www.google.com/search?q=kerala&rlz=1C5CHFA_enIN988IN988&oq=ker&aqs=chrome.0.35i39j46i433i512j69i57j69i60l5.1347j0j7&sourceid=chrome&ie=UTF-8')
    link=models.URLField()
    district=models.ForeignKey(districts,on_delete=models.CASCADE)
    type=models.ForeignKey(remark,on_delete=models.CASCADE)
    warning=models.TextField(help_text='give any special advise or any special local warning here')
    key_words=models.TextField(help_text='keyword must start with %,keywords give your contribution more expo!')
    date=models.DateTimeField(auto_now_add=True)
    verify=models.BooleanField(default=False)
    

    #rating=models.FloatField(default=5)
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
    content=models.TextField()
    status=models.CharField(max_length=12,choices=(('visited','visited'),('Not visited','Not visited')))
    rating=models.CharField(max_length=14,choices=(('Below average','Below average'),('Average', 'Average'),('Recomandable', 'Recomandable'),('Good','Good'),('fentastic','fentastic')),blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)
    spot=models.ForeignKey(spot,on_delete=models.CASCADE,related_name='reviewmodel')
    def __str__(self):
        return str(self.spot)
    
