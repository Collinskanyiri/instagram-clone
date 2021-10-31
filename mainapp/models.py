from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(max_length=500)
    profile_photo = CloudinaryField('image')
    

    def __str__(self):
        return self.user.username 

    def save_profile(self):
        self.save()

    def update_profile(self,):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return profile

class Image(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='images')
    image= CloudinaryField('image') 
    image_name=models.CharField(max_length=60)
    image_date = models.DateTimeField(auto_now_add=True,)
    image_caption = models.TextField(blank=True)
    likes=models.IntegerField(default=0)
    comments=models.IntegerField(default=0)

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def update_image(self):
        self.update_image()

    @classmethod
    def get_images_by_user(cls, user):
        images = cls.objects.filter(user=user)
        return images

    @classmethod
    def search_by_image_name(cls, search_term):
        images = cls.objects.filter(
            image_name__icontains=search_term)
        return images

    @classmethod
    def get_single_image(cls, id):
        image = cls.objects.get(id=id)
        return image

class Comment(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.CharField(max_length=60)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

class Likes(models.Model):
    image=models.ForeignKey(Image, on_delete=models.CASCADE, related_name='images')
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
       return self.likes 
