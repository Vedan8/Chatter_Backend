from django.db import models
from core.models import User
from cloudinary.models import CloudinaryField
import cloudinary
from django.core.files.uploadedfile import InMemoryUploadedFile


class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    postImage=CloudinaryField('image')
    description=models.TextField()
    likes=models.IntegerField(default=0,blank=True)

    def save(self, *args, **kwargs):
        # Upload the image to Cloudinary
        if isinstance(self.postImage, InMemoryUploadedFile):  # Ensure it's an in-memory file
            upload_result = cloudinary.uploader.upload(self.postImage)

            # Get the public_id and secure_url from the Cloudinary response
            self.postImage = upload_result.get('secure_url') 

            # Optionally, you can store the URL in a separate field if needed
            # self.image_url = full_url

        super(Posts, self).save(*args, **kwargs)  

class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.TextField()
