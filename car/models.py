from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'

class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    picture = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.brand} {self.name}'

class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length=50)
    description = models.TextField()
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    parches_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} {self.car.name}'
    
