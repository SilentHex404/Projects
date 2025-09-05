from django.db import models
import uuid

class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField(blank=False,null=False)
    manager = models.OneToOneField('user.User', related_name='team_manager' , on_delete=models.CASCADE , null=False , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name