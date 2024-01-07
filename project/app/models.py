from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Product(models.Model):
    product_name = models.CharField(max_length=120, unique=True)
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',
    )
    quantity = models.IntegerField(default=0)
    price = models.FloatField(validators=[MinValueValidator(0.0)],)
    description = models.TextField()

    def __str__(self):
        return f'{self.product_name.title()}: {self.description[:20]}'
    #get_absolute_url сделан для чтобы после создания продукта нас перекидывало на страничку с этим id
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()
