from django.db import models
from core.models import User
from cloudinary.models import CloudinaryField
import cloudinary
from django.core.files.uploadedfile import InMemoryUploadedFile

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postImage=CloudinaryField('image', null=True, blank=True)
    imageUrl = models.URLField(max_length=500, blank=True, null=True) 
    description = models.TextField()
    likes = models.IntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        if isinstance(self.postImage, InMemoryUploadedFile):
            upload_result = cloudinary.uploader.upload(self.postImage)
            self.imageUrl = upload_result.get('secure_url')

        super(Posts, self).save(*args, **kwargs)

    @property
    def isLiked(self):
        """
        This property checks if the logged-in user has liked the post.
        """
        request = getattr(self, '_request', None)
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=self).exists()
        return False

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.TextField()
