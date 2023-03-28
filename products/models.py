from django.db import models
from django.utils.html import mark_safe
import os
from django.contrib.auth.models import AbstractUser,User

# Create your models here.

def get_file_path(self, filename,*args,**kwargs):
            #this function is use to store the img in images/product/brandname/image.jpg
            print("Product IMAGE: : ",self.product.product_brand.brand_title)
            img=self.product.product_brand.brand_title
            path='images/product_imgs/'+img
            return os.path.join(path,filename)






#Brand
class Brands(models.Model):
    brand_title = models.CharField("PRODUCT NAME",max_length=255,)
    b_slug = models.SlugField(max_length = 150)
    brand_img= models.ImageField(upload_to='images/brand_imgs',null=True,blank=True)
    # tumbnail=models.ImageField(upload_to='images/brand_imgs',null=True,blank=True)
    def get_absolute_url(self):
        return f'/{self.b_slug}/'
    
    def get_image(self):
        if self.brand_img:
            return 'http://127.0.0.1:8000' + self.brand_img.url
        return ''

    def __str__(self):
        return self.brand_title
    
#Product
class Products(models.Model):
    p_slug = models.SlugField(max_length = 150)
    product_name=models.CharField(max_length=255)
    product_brand=models.ForeignKey(Brands,on_delete=models.CASCADE,related_name="brand")
    product_img=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    price=models.PositiveIntegerField(default=0)
    def get_img(self):
        if self.img_brand:
            return 'http://127.0.0.1:8000/' + self.product_img.url
        return ''




    def get_absolute_url(self):
        return f'/{self.p_slug}/'
   
    def __str__(self):
        return self.product_name  

#color
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    
#Size
class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    

#variants

class Variants(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Imaget.objects.get(id=self.image_id)
        print('++++++++++++++++++++++++++++++',self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Imaget.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""



#Image
class Imaget(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name = "images")
    image= models.ImageField(upload_to=get_file_path,null=True,blank=True)
    is_default = models.BooleanField(default=False)
    


    #it will return image url
    def get_img(self):
        if self.img_brand:
            return 'http://127.0.0.1:8000/' + self.img_brand.url
        return ''



   
    