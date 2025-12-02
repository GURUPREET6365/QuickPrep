from django.db import models
from Notes.models import File
from django.contrib.auth.models import User

# Create your models here.
class Questions(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=600)
    A = models.CharField(max_length=255)
    B = models.CharField(max_length=255)
    C = models.CharField(max_length=255)
    D = models.CharField(max_length=255)

    CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    """
    Now we made a choices of list that contains tuples.
    This tuple has format contains what to store in the db and what to show in the admin panel.
    """

    answer = models.CharField(max_length=255, choices=CHOICES)

    

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user