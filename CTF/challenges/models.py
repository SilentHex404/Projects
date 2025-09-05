from django.db import models
import uuid

class Challenge(models.Model):
    id = models.UUIDField(default=uuid.uuid4 , editable=False , null=False , unique=True , primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    score = models.IntegerField(default=0)
    creator = models.ForeignKey("user.User", on_delete=models.CASCADE, null=False, related_name="created_challenges")
    solved_by = models.ManyToManyField("user.User", through="SolvedChallenge", related_name="solved_challenges")
    flag = models.CharField(max_length=100)
    ChallFile = models.FileField(upload_to='ChallFiles/', max_length=100 ,blank=False , null=True)

    def __str__(self):
        return self.name


class SolvedChallenge(models.Model):
    id = models.UUIDField(default=uuid.uuid4 , editable=False , null=False , unique=True , primary_key=True)
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE, related_name="solves")
    solved_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="challenge_solves")
    solved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.challenge} solved by {self.solved_by}"
