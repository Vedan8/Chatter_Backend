from django.db import models
from core.models import User
from cloudinary.models import CloudinaryField
import cloudinary
from django.core.files.uploadedfile import InMemoryUploadedFile


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postImage = CloudinaryField('image')  # CloudinaryField to handle the uploaded file
    imageUrl = models.URLField(max_length=500, blank=True, null=True)  # URLField to store the full Cloudinary URL
    description = models.TextField()
    likes = models.IntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        # Upload the image to Cloudinary if it's an InMemoryUploadedFile
        if isinstance(self.postImage, InMemoryUploadedFile):
            upload_result = cloudinary.uploader.upload(self.postImage)

            # Store the secure_url in the imageUrl field
            self.imageUrl = upload_result.get('secure_url')

        super(Posts, self).save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.TextField()
