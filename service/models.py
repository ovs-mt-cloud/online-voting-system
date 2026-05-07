from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    username=models.CharField(max_length=10)
    email=models.CharField(max_length=20)
    add=models.TextField()

from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=255)
    college = models.CharField(max_length=200)  # 👈 IMPORTANT
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.option_text


# NEW MODEL
class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ('poll', 'ip_address')


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username