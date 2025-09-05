from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser) :
    id = models.UUIDField(default=uuid.uuid4 , unique=True , editable=False , primary_key=True , null=False)
    username = models.CharField(max_length=50 , blank=False , null=False , unique=True)
    email = models.EmailField(max_length=254 , blank=False , null=False , unique=True)
    team = models.ForeignKey('team.Team', related_name='team_members', on_delete=models.SET_NULL , blank=True , null=True)
    created_challs = models.IntegerField(default=0)
    solved_challs = models.IntegerField(default=0)
    first_bloods = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username