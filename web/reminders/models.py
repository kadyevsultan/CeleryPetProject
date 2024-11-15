import random
import string

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Reminder(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500,blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    date = models.DateTimeField()
    slug = models.SlugField('URL', max_length=250, unique=True, blank=True)
    
    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'
    
    def __str__(self):
        return self.title
    
    @staticmethod
    def _rand_slug():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self._rand_slug() + '-' + self.title)
        super().save(*args, **kwargs)
        
