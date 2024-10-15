from django.db import models
from django.utils.text import slugify


class Livreto(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    system = models.CharField('Sistema', max_length=200, choices=(('marquefacil', 'Marque Facil'), ('observatorio', 'Observatório')))
    pdf = models.FileField(upload_to='livretos/')
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def json(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "system": self.system,
        }