from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

User = get_user_model()

def upload_post_image(instance, filename):
    return f"{instance.user}/{filename}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now=True)  # should be auto_now_add
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField() # markdown 
    thumbnail = models.ImageField(upload_to=upload_post_image)

    def __str__(self):
        return self.title

def pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_receiver, sender=Post)