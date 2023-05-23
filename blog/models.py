from django.db import models



from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel
from PIL import Image
import os
from django.conf import settings


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


class Municipio(TimeStampedModel):
    nome = nome = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="nome")

    class Meta:
        ordering = ("nome",)
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("products:list_by_municipio", kwargs={"slug": self.slug})

class Categoria(TimeStampedModel):
    nome = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="nome")

    class Meta:
        ordering = ("nome",)
        verbose_name = "Categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("products:list_by_categoria", kwargs={"slug": self.slug})


class Noticia(TimeStampedModel):
    categoria = models.ForeignKey(
        Categoria, related_name="noticias", on_delete=models.CASCADE, verbose_name="Categoria")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    titulo = models.CharField(max_length=255, verbose_name="titulo")
    slug = AutoSlugField(unique=True, always_update=False, populate_from="titulo")
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, verbose_name="Imagem da capa")
    descricao = models.CharField(max_length=300, blank=True)
    informacao = models.TextField(blank=True)   
    type = models.CharField(
        default = "V",
        max_length = 1,
        choices =(
            ('S', 'VARIAÇÃO'),
            ('N', 'NONE'),
        )
    )
    
    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        
        if original_width <= new_width:            
            img_pil.close()
            
        new_height = round((new_width * original_height) / original_width)
        
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
        
        
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        max_image_size = 800
        
        if self.image:
            self.resize_image(self.image, max_image_size)
            
    
    is_available = models.BooleanField(default=True)

    objects = models.Manager()
    available = AvailableManager()

    class Meta:
        list_by_category = ("nome",)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
    
    class Meta:        
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"