
# Create your models here.
# slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

from django.db import models
from django.urls import reverse

class Products(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, blank=True, default='')
    parameter = models.TextField(blank=True, verbose_name="Текст статьи")
    price = models.CharField(max_length=50, verbose_name="Цена")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts", verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'
        ordering = ['title', '-price']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    #     # return reverse('catalog', kwargs={'cat_slug': self.slug})


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

