from django.db import models
from accounts.models import User
from menu.models import FoodItem


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # user is foreignkey, thats why the unicode instead of __str__
    def __unicode__(self):
        return self.user

