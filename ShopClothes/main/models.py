from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import re

def slugify_cyrillic(value):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    value = value.lower()
    value = ''.join(translit_dict.get(c, c) for c in value)
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return slugify(value)

class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    size = models.CharField(max_length=4, choices=SIZE_CHOICES)
    title=models.CharField(max_length=100)
    image=models.ImageField(default='img/default.jpg',upload_to='img/')
    price=models.PositiveIntegerField()
    description=models.TextField(max_length=500)
    slug=models.SlugField(blank=True,unique=True)
    category=models.ForeignKey('Category',on_delete=models.PROTECT)
    brand=models.ForeignKey('Brand',on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Category(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(blank=True,unique=True)

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Brand(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(blank=True,unique=True)
    image=models.ImageField(default='img/default.jpg',upload_to='img/')

    def get_absolute_url(self):
        return reverse("brand", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title