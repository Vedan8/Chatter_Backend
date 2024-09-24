from django.db import models
from core.models import User
class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    postImage=models.ImageField(default="https://img.icons8.com/?size=64&id=tZuAOUGm9AuS&format=png")
    description=models.TextField()
    likes=models.IntegerField(default=0,blank=True)

class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.TextField()
