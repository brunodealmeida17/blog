from django.db import models

from django.db import models
from django.conf import settings
import os
from PIL import Image
from django.db import models


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)

class ImagesDestaque(models.Model):
    campanha = models.CharField(max_length=200, )
    destaque = models.ImageField(upload_to="destaque/%Y/%m/%d", blank=True)
    link = models.CharField(max_length=300, blank=True, null=True, verbose_name='link de acesso')
    
    @staticmethod
    def resize_image(img, new_width=2000):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        
        
            
        new_height = round((new_width * original_height) / original_width)
        
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
        
        
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        max_image_size = 2000
        
        if self.destaque:
            self.resize_image(self.destaque, max_image_size)

    is_available = models.BooleanField(default=True, verbose_name="Esse destaque esta ativo?")
    
    objects = models.Manager()
    available = AvailableManager()
            
    def __str__(self):
        return self.campanha
    
    
    
    class Meta: 
        verbose_name = "Destaque"
        verbose_name_plural = "Imagens de destaque"