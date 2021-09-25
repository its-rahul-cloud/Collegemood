from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import random

def random_string():
    return str(str(random.randint(1, 10))+".jpeg")


class College(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'collegeimg')
    about = models.TextField(max_length=400)
    def __str__(self):
        return str(self.id)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    college_name  = models.CharField( max_length=200)
    Branch_Year = models.CharField(max_length=2,default= 2)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    location = models.CharField(max_length=50)
    skill = models.CharField(max_length=200,default='Sleeping')
    profession = models.CharField(max_length=200,default='Student')
    
    
    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


Type=(('StudyMaterial','StudyMaterial'),
('Information','Information'))

class Post(models.Model):
    type = models.CharField(max_length=60,choices=Type,default='Information')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=400)
    content = models.TextField(max_length=4000)
    image = models.ImageField( upload_to = 'post',default =random_string)
    pdf = models.FileField(upload_to='pdfs',default ="defaultpost.jpeg",null=True,blank = True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



def create_user_profile(sender, instance, created, **kwargs):
    """
    :param sender: Class User.
    :param instance: The user instance.
    """
    if created:
        # Seems the following also works:
        #   UserProfile.objects.create(user=instance)
        #  TODO: Which is correct or better?
        profile = Profile(user=instance)
        profile.save()

post_save.connect(create_user_profile,
                  sender=User,
                  dispatch_uid="users-profilecreation-signal")

class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=1000)


    def __str__(self):
        return str(self.id)



